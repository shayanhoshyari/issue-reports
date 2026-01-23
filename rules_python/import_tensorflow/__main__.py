import tensorflow as tf

print(f"TensorFlow version: {tf.__version__}")
gpus = tf.config.list_physical_devices("GPU")
print(f"TF devices (GPU): {gpus}")
