import json
import ast


with open("/home/tsitoand/Downloads/test(1).json", "r") as f:
    file = json.load(f)
    
print("outpout = ", len(file))

with open("my_test_call.json", "r") as fb:
    file_b = json.load(fb)
    
print("call = ", len(file_b))

