import os
from tensorflow.python import pywrap_tensorflow

checkpoint_path = os.path.join('./my_net/', "save_net.ckpt")
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
param_dict = reader.get_variable_to_shape_map()
print(param_dict)
