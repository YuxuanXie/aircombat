import os
from tensorflow.python import pywrap_tensorflow

# checkpoint_path = os.path.join('./my_net_new/', "save_net.ckpt")
checkpoint_path = './log/model/2021-10-08-15-52-32/570000.ckpt'
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
param_dict = reader.get_variable_to_shape_map()

f = open('model.txt', 'w')

for key in var_to_shape_map:
    if key ==  "eval_net/l1/w1":
        print(" ")
        print("tensor_name: ", key, file=f)
        # print(reader.get_tensor(key))
        data = reader.get_tensor(key)
        s = ''
        for i in range(64):
            for j in range(32):
                s += f'{data[j][i]},'
        print(s, file=f)

    if key ==  "eval_net/l2/w2":
        print(" ")
        print("tensor_name: ", key, file=f)
        # print(reader.get_tensor(key))
        s = ''
        for i in range(64):
            for j in range(10):
                s += f'{reader.get_tensor(key)[i][j]},'
        print(s, file=f)

    if key == "eval_net/l1/b1":
        print(" ")
        print("tensor_name: ", key, file=f)
        # print(reader.get_tensor(key))
        s = ''
        for i in range(64):
            s += f'{reader.get_tensor(key)[0][i]},'

        print(s, file=f)

    if key == "eval_net/l2/b2":
        print(" ")
        print("tensor_name: ", key, file=f)
        # print(reader.get_tensor(key))
        s = ''
        for i in range(10):
            s += f'{reader.get_tensor(key)[0][i]},'
        print(s, file=f)
f.close()
