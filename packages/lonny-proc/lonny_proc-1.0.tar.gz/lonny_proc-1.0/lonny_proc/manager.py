from multiprocessing import Process
from .policy import Policy
from .logger import logger
from time import sleep
from signal import signal, SIG_IGN, SIGINT, SIGTERM

class Context:
    alive = None
    proc_id = None

def _handle(_sig, _frame):
    Context.alive = False

class Manager:
    def __init__(self, *, policy = Policy.never):
        self._specs = list()
        self._procs = dict()
        self._policy = policy

    def add(self, target, *, args = ()):
        proc_id = len(self._specs)
        def wrapper(*args, **kwargs):
            Context.alive = True
            Context.proc_id = proc_id
            signal(SIGINT, SIG_IGN)
            signal(SIGTERM, _handle)
            target(*args, **kwargs)
        self._specs.append((wrapper, args))

    def _should_restart(self, is_error):
        if self._policy == Policy.always:
            return True
        return self._policy == Policy.unless_error and not is_error

    def tick(self):
        for ix, (target, args) in enumerate(self._specs):
            proc = self._procs.get(ix)
            if proc is None:
                logger.info(f"Starting process: {ix}.")
                proc = Process(target = target, args = args)
                self._procs[ix] = proc
                proc.start()
            elif not proc.is_alive():
                if self._should_restart(proc.exitcode != 0):
                    logger.info(f"Restarting process: {ix}. Exit code: {proc.exitcode}.")
                    proc = Process(target = target, args = args)
                    self._procs[ix] = proc
                    proc.start()
                else:
                    err_msg = f"Process: {ix} stopped with exit code: {proc.exitcode} and cannot recover."
                    logger.error(err_msg)
                    raise RuntimeError(err_msg)
    
    def __enter__(self):
        return self

    def __exit__(self, _value, _type, _traceback):
        for ix, proc in self._procs.items():
            if not proc.is_alive():
                continue
            logger.debug(f"Sending SIGTERM to process: {ix}.")
            proc.terminate()
        for ix, proc in self._procs.items():
            logger.debug(f"Joining process: {ix}")
            proc.join()

