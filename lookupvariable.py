import os
import numpy as np
from tensorflow.python import pywrap_tensorflow

for i in range(4):
    checkpoint_path = f'./log/model/2021-10-19-15-51-18/385000_agent{i}.ckpt'
    reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
    var_to_shape_map = reader.get_variable_to_shape_map()
    param_dict = reader.get_variable_to_shape_map()

    file_name= f'model_agent{i}.bin'

    output_keys = ["eval_net/l1/b1", "eval_net/l2/b2", "eval_net/l1/w1", "eval_net/l2/w2"]
    s = []
    for key in output_keys:
        if key ==  "eval_net/l1/w1":
            print(" ")
            # print("tensor_name: ", key, file=f)
            # print(reader.get_tensor(key))
            data = reader.get_tensor(key)
            for i in range(64):
                for j in range(32):
                    s.append(data[j][i])

        if key ==  "eval_net/l2/w2":
            print(" ")
            # print("tensor_name: ", key, file=f)
            # print(reader.get_tensor(key))
            for i in range(64):
                for j in range(10):
                    s.append(reader.get_tensor(key)[i][j])

        if key == "eval_net/l1/b1":
            print(" ")
            # print("tensor_name: ", key, file=f)
            # print(reader.get_tensor(key))
            for i in range(64):
                s.append(reader.get_tensor(key)[0][i])


        if key == "eval_net/l2/b2":
            print(" ")
            # print("tensor_name: ", key, file=f)
            # print(reader.get_tensor(key))
            for i in range(10):
                s.append(reader.get_tensor(key)[0][i])
    model = np.array(s, dtype=float)
    print(f"{file_name} = {model.shape}")
    model.tofile(file_name)
