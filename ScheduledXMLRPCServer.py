from SimpleXMLRPCServer import SimpleXMLRPCServer
import select

class ScheduledXMLRPCServer(SimpleXMLRPCServer):
    """
    Allow SimpleXMLRPCServer instance to schedule a function at _sleep_-second
    intervals, with resolution of _poll_interval_ seconds.
    """
    
    task = None
    sleep = 0
    
    @staticmethod
    def _eintr_retry(func, *args):
        """restart a system call interrupted by EINTR"""
        while True:
            try:
                return func(*args)
            except (OSError, select.error) as e:
                if e.args[0] != errno.EINTR:
                    raise
    
    def register_task(self, f, sleep=60):
        self.task = f
        self.sleep = sleep
    
    def serve_forever(self, poll_interval=0.5):
        c = 0
        self._BaseServer__is_shut_down.clear()
        try:
            while not self._BaseServer__shutdown_request:
                if self.task and poll_interval:
                    c = (c + 1) % (self.sleep / poll_interval)
                    if c == 0:
                        self.task()
                r, w, e = self._eintr_retry(select.select, [self], [], [],
                                       poll_interval)
                if self in r:
                    self._handle_request_noblock()
        finally:
            self._BaseServer__shutdown_request = False
            self._BaseServer__is_shut_down.set()

if __name__ == '__main__':
    from datetime import datetime as dt
    
    class maths:
        def add(self, x, y):
            return x + y
            
    def now():
        print dt.now()

    server = ScheduledXMLRPCServer(("localhost", 8000))
    server.register_instance(maths())
    server.register_task(now, 3)

    try:
        server.serve_forever(poll_interval=1)
    except KeyboardInterrupt:
        server.shutdown()
