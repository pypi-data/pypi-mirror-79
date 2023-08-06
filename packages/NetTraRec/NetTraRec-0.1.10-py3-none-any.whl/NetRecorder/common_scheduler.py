import sys
import threading
import traceback


class ComThread(threading.Thread):
    def __init__(self, function, params):
        threading.Thread.__init__(self)
        self.func = function
        self.params = params

    def run(self):
        try:
            return self.func(**self.params)
        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            print(f"error in running common thread: ({str(self.func)}):\n{E}\n\n{err}")
