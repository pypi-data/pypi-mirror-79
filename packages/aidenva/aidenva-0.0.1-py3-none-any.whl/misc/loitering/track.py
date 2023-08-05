import time

class Track:

    def __init__(self,_id,_box,_confidence,class_id=1):
        self.box=_box
        self.created_time=time.time()
        self.confidence=_confidence
        self.id=_id
        self.class_id=class_id