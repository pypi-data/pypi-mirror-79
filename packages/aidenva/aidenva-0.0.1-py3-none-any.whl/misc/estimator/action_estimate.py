
from misc.estimator.cqueue import cQueue
import numpy as np

class ActionFrameEstimate:
    def __init__(self, size=16):
        self.size = size
        self.f_queue = q = cQueue(size)

    def add_frame(self, f, boxs):
        self.f_queue.enqueue([f, boxs])

    def frames(self):
        return list(reversed(np.array(self.f_queue._queue)[:, 0]))

if __name__ == '__main__':
    action = ActionFrameEstimate()

    action.add_frame(0, 0)
    action.add_frame(1, 1)
    action.add_frame(2, 2)
    action.add_frame(3, 3)

    print(list(reversed(action.frames())))

