import json

with open("/home/tsitoand/Desktop/call_me_maybe/src/functions_definition.json", "r") as f:
    def_ft = json.load(f)

ft = def_ft[4]

for par in ft['parameters']:
    print(ft['parameters'][par]['type'])