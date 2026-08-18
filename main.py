from src.llm_sdk import Small_LLM_Model
import sys
import json
import math
import re

with open("src/function_calling_tests.json", "r") as test_file:
    data = json.load(test_file)


with open("src/functions_definition.json", "r") as f:
    ft_list: list[dict] = json.load(f)




model = Small_LLM_Model()

print(model.get_path_to_vocab_file())

name = []



msg = data[0]['prompt']
print(msg)

ex = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.0}}'

prompt = f"""
Your task is to select the appropriate function from the available functions
and extract its arguments from the user's request.

Available functions:
{ft_list}

Example:
User request: 'what's the sum of 2 and 3'
Output: {ex}

User request: {msg}

Output:
"""


def level_breaker(s: str) -> bool:
    l = 0

    for i in s:
        if i == '{':
            l += 1
        if i == '}':
            l -= 1
    if not s:
        return False
    
    if l == 0:
        print("our time as come")
        return True
    return False


ft_name = [ft['name'] for ft in ft_list]


name = [x for ft in ft_list for x in model.encode(ft['name'])[0].tolist()]
name = list(set(name))
name.append(1)
# print("from here")
# print(anarana)
# print("to here")

# name.append(model.encode("\"")[0].tolist())


# constrainte


# name
# def constrainte_name(ids: list[float], d: list[list[int]]):
#     while True:
#         next = ids.index(max(ids))
#         if any(next in line for line in name):
#             break

#         ids[next] = -math.inf
#     return next

# type

#number

def get_name(ids: list[float], valid: list):
    for i in range(len(ids)):
        if i not in valid:
            ids[i] = -math.inf


template = '{"name": "'



# recherche name

tokens1  = model.encode(prompt)
tokens = tokens1[0].tolist()
tokens += model.encode(template)[0].tolist()

txt = ""
txt += template

b = False


with open("/home/tsitoand/Desktop/vocab.json", "r") as f:
    vocab = json.load(f)

number = [vocab[i] for i in vocab if re.search("^[0-9\+\-]$", i)]


for _ in range(10):
    log = model.get_logits_from_input_ids(tokens)
    # constrainte_name(log, name)


    get_name(log, name)
    next = log.index(max(log))
    tokens.append(next)
    txt += model.decode(next)
    if next == 1:
        b = True
        break

    print(txt)
    print("--------------------------------------")

else:
    print("Error infinite loop")
    sys.exit(-1)

if b:
    print(txt)
x = ',"parameters": {"'
tokens += model.encode(x)[0].tolist()

n = txt.split("\"")[3]
if n not in ft_name:
    print("invalide name")

else:
    tokens += model.encode(", \"arguments\": {")[0].tolist()
    t = ", \"arguments\": {"
    txt += t
    print(f"found {n}")

    for j in ft_list:
        if j['name'] == n:
            x = j

    # print(x)
        par = x['parameters']
        
    for i in par:

        print(i, par[i]['type'])
        





# # recherche parametre
# txt += x
# print(txt)
# print("--------------------------------------")
# for _ in range(50):
#     log = model.get_logits_from_input_ids(tokens)
#     next = log.index(max(log))
#     # constrainte_name(log, name)
#     tokens.append(next)
#     txt += model.decode(next)
#     if level_breaker(txt):
#         print(txt)
#         print("--------------------------------------")
#         break

#     if next == 92:
#         print(txt)
#         print("--------------------------------------")
#         break
#     print(txt)
#     print("--------------------------------------")