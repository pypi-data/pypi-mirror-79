import threading


class BaseEntropySource(object):
    def __init__(self, buffer):
        self.buffer = buffer
        self.is_running = True
        self.thread = threading.Thread(target=self.start_collecting_entropy)
        self.thread.start()

    def start_collecting_entropy(self):
        pass

    def stop_collecting_entropy(self):
        pass

    def release(self):
        self.is_running = False
        self.stop_collecting_entropy()
