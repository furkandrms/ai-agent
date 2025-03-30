import sys 
import threading
from io import StringIO


class StreamlitLogger:
    def __init__(self): 
        self.buffer = StringIO()
        self.lock = threading.Lock()

    def write(self, message):
        with self.lock:
            self.buffer.write(message)
            sys.stdout.flush()
    
    def flush(self): 
        pass

    def get_value(self): 
        with self.lock: 
            return self.buffer.getvalue()