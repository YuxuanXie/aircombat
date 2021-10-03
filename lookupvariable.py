import os
from tensorflow.python import pywrap_tensorflow

checkpoint_path = os.path.join('./my_net_new/', "save_net.ckpt")
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
param_dict = reader.get_variable_to_shape_map()
print(param_dict)
for key in var_to_shape_map:
    if key ==  "eval_net/l1/w1":
        print(" ")
        print("tensor_name: ", key)
        print(reader.get_tensor(key))
        for i in range(64):
            for j in range(32):
                print(reader.get_tensor(key)[j][i],end=',')
    if key ==  "eval_net/l2/w2":
        print(" ")
        print("tensor_name: ", key)
        print(reader.get_tensor(key))
        for i in range(64):
            for j in range(10):
                print(reader.get_tensor(key)[i][j],end=',')
    if key == "eval_net/l1/b1":
        print(" ")
        print("tensor_name: ", key)
        print(reader.get_tensor(key))
        for i in range(64):
            print(reader.get_tensor(key)[0][i],end = ",")
    if key == "eval_net/l2/b2":
        print(" ")
        print("tensor_name: ", key)
        print(reader.get_tensor(key))
        for i in range(10):
            print(reader.get_tensor(key)[0][i], end=",")