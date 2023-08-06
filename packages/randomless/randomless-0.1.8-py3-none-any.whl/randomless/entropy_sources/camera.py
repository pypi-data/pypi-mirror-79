from randomless.entropy_sources.base_entropy_source import BaseEntropySource
import cv2
import numpy as np


class CameraEntropySource(BaseEntropySource):
    def __init__(self, buffer):
        super().__init__(buffer)
        self.cap = None

    def start_collecting_entropy(self):
        bits_per_value = 8
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                frame = frame.reshape(frame.shape[0]*frame.shape[1]*frame.shape[2])
                frame = frame[0:frame.shape[0] - (frame.shape[0] % bits_per_value)]
                frame = frame.reshape((bits_per_value, frame.shape[0] // bits_per_value))
                frame = frame % 2
                for i in range(7):
                    frame[i+1] *= 2**(i+1)
                frame = frame.sum(axis=0).astype(np.uint8)
                frame = frame.tobytes()
                frame = [frame[i:i + 1] for i in range(len(frame))]
                self.buffer.enqueue(frame)

    def stop_collecting_entropy(self):
        self.cap.release()
