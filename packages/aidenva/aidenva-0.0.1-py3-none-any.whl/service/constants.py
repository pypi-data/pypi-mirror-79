import tensorflow as tf

# 0.67 would allocate 67% of GPU memory for TensorFlow, making the remaining 33% available for TensorRT engines
_GPU_MEM_FRACTION = 0.67

# DEFINDED VA TYPES
NONE            = 0b00000000000000000000  # DUMMY
DETECT_VA       = 0b00000000000000000001  # PERSON DETECTION
FALLDOWN_VA     = 0b00000000000000000010  # FALLDOWN DETECTION
HARNESS_VA      = 0b00000000000000000100  # HARNESS DETECTION
HELMET_VA       = 0b00000000000000001000  # HELMET DETECTION
FIRESMOKE_VA    = 0b00000000000000010000  # SMORKE DETECTION
INTRUSION_VA    = 0b00000000000000100000  # INTRUSION DETECTION
CCTVEXC_VA      = 0b00000000000001000000  # INTRUSION DETECTION
LOITERING_VA    = 0b00000000000010000000  # LOITERING
TRACKING_VA     = 0b00000000000100000000  # TRACKING_VA
CLUSTER_VA      = 0b00000000001000000000  # CLUSTER_VA
CROSSLINE_VA    = 0b00000000010000000000  # CROSSLINE_VA


# config va_engines name mapping
DETECT_VA_NAME     = 'detect'
FALLDOWN_VA_NAME   = 'falldown'
HARNESS_VA_NAME    = 'harness'
HELMET_VA_NAME     = 'helmet'
FIRESMOKE_NAME     = 'firesmoke'
INTRUSION_NAME     = 'intrusion'
CCTVEXC_NAME       = 'cctvexc'
LOITERING_NAME     = 'loitering'
TRACKING_NAME      = 'tracking'
CLUSTER_NAME       = 'cluster'
CROSSLINE_NAME     = 'crossline'

VA_TYPES = {
    DETECT_VA: DETECT_VA_NAME,
    FALLDOWN_VA:FALLDOWN_VA_NAME,
    HARNESS_VA:HARNESS_VA_NAME,
    HELMET_VA:HELMET_VA_NAME,
    FIRESMOKE_VA:FIRESMOKE_NAME,
    INTRUSION_VA: INTRUSION_NAME,
    CCTVEXC_VA: CCTVEXC_NAME,
    LOITERING_VA: LOITERING_NAME,
    TRACKING_VA: TRACKING_NAME,
    CROSSLINE_VA: CROSSLINE_NAME,
    CLUSTER_VA: CLUSTER_NAME
}

VA_NAMES = {y.upper():x for x,y in VA_TYPES.items()}

# deep-learning method defined
INF_METHOD_DETECTION = 0
INF_METHOD_CLASSIFICATION = 1
INF_METHOD_SEGMENTATION = 2

# bit check type
def check_va_type(check, va_type):
    return bool(check & va_type)

def get_gpu_options(config):
    gpu_options = tf.compat.v1.GPUOptions(per_process_gpu_memory_fraction=config.getvalue('va_engines.gpu_mem_fraction', _GPU_MEM_FRACTION))
    # gpu_options.allow_growth = True
    return tf.compat.v1.ConfigProto(gpu_options=gpu_options)

if __name__ == '__main__':
    print(VA_NAMES)