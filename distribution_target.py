def perm(arr):
    """实现全排列"""
    length = len(arr)
    if length == 1:  # 递归出口
        return [arr]

    result = []  # 存储结果
    fixed = arr[0]
    rest = arr[1:]

    for _arr in perm(rest):  # 遍历上层的每一个结果
        for i in range(0, length):  # 插入每一个位置得到新序列
            new_rest = _arr.copy()  # 需要复制一份
            new_rest.insert(i, fixed)
            result.append(new_rest)
    return result
def indexofMin(arr):
    minindex = 0
    currentindex = 1
    while currentindex < len(arr):
        if arr[currentindex] < arr[minindex]:
            minindex = currentindex
        currentindex += 1
    return minindex
if __name__ == '__main__':
    r = perm([1,2,3])
    for i in r:
        print(i)
    arr = [3, 5, 2, 1]
    print(indexofMin(arr))
