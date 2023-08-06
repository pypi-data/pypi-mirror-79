from base_random import BaseRandom
from entropy_sources.camera import CameraEntropySource


class Random(BaseRandom):
    def __init__(self, entropy_sources_list=['camera'], buffer_size=2**20):
        super().__init__(buffer_size)
        self.entropy_sources = []
        for s in entropy_sources_list:
            self.entropy_sources.append(entropy_source_names[s](self.buffer))

    def release(self):
        for s in self.entropy_sources:
            s.release()


entropy_source_names = {
    'camera': CameraEntropySource
}
