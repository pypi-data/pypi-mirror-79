import os
import os.path

path = os.getcwd()

#for file in os.listdir(path):
#     if file.endswith(".py"):
#         print(file)

file = [filename for filename in os.listdir(path) if filename.endswith(".py")]

for files in file:
    print(files)