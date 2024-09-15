import numpy as np

file = open("datasets/input.txt", "r")

data = file.read()

data_list = list(data)

print("".join(data_list[2:5]))
#print(list(data))
