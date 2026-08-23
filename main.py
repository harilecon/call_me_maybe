from src.llm_sdk.llm_sdk import Small_LLM_Model
import sys
import json
import math
import re
# /home/tsitoand/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca/vocab.json


model = Small_LLM_Model()
vocab = model.get_path_to_vocab_file()

def main(msg):

    with open("src/functions_definition.json", "r") as f:
        ft_list: list[dict] = json.load(f)


    name = []


    print(msg)

    ex = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.5}}'

    prompt = f"""
    Your task is to select the appropriate function from the available functions
    and extract its arguments from the user's request.

    Available functions:
    {ft_list}

    Example:
    User request: 'what's the sum of 2,0 and 3,5'
    Output: {ex}

    User request: {msg}

    Output:
    """


    # ft_name = [ft['name'] for ft in ft_list]

    name = [x for ft in ft_list for x in model.encode(ft['name'])[0].tolist()]
    name = list(set(name))
    name.append(1)
    name += [1]



    def mask_token(ids: list[float], valid: list):
        for i in range(len(ids)):
            if i not in valid:
                ids[i] = -math.inf


    # template = '{"name": "'
    template = model.encode('{"name": "')[0].tolist()


    txt = []
    # # # recherche name

    tokens = model.encode(prompt)[0].tolist()
    txt += model.encode('{"name": "')[0].tolist()
    tokens += txt



    with open(model.get_path_to_vocab_file(), "r") as f:
        vocab = json.load(f)



    def search_variable_number(tokens, txt: list, constraint):

        for _ in range(100):
            ids = model.get_logits_from_input_ids(tokens)

            next = ids.index(max(ids))
            if next == 11:
                break
            if constraint:
                mask_token(ids, constraint)

            txt.append(next)
            tokens.append(next)
            try:
                x = model.decode(txt)
                print(x)
                json.loads(x)
                break
            except Exception:
                ...
            
        return (tokens, txt)



    # def search_variable_name(tokens, txt: list, constraint):

    #     for _ in range(10):
    #         ids = model.get_logits_from_input_ids(tokens)

    #         next = ids.index(max(ids))
    #         if next == 1:
    #             break
    #         if constraint:
    #             mask_token(ids, constraint)

    #         txt.append(next)
    #         tokens.append(next)
    #         try:
    #             x = model.decode(txt)
    #             print(x)
    #             return(json.loads(x))
    #             break
    #         except Exception:
    #             print("merde on remet ca")
    #             ...

    #     return (tokens, txt)

    def search_name(tokens, txt: list, constraint):
        for _ in range(10):
            ids = model.get_logits_from_input_ids(tokens)


            mask_token(ids, constraint)
            next = ids.index(max(ids))
            tokens.append(next)
            txt.append(next)
            try:
                x = model.decode(txt)
                json.loads(x)
                break
            except Exception:
                ...

            if next == 1:
                break

            print(x)

        return (tokens, txt)

    tokens, txt =  search_name(tokens, txt, name)

    # for j in ft_list:
    #     if j['name'] == name:
    #         x = j
    parameter = model.encode(', "parameters": {')[0].tolist()
    tokens += parameter
    txt += parameter

    # par = x['parameters']


    constraint = {
        'string': None,
        'number': [vocab[i] for i in vocab if re.search("^[0-9\-\+.\,}\"]$" ,i)]
        }

    # txt = '{"name": "fn_add_numbers", "parameters": {'
    # tokens += model.encode('{"name": "fn_add_numbers", "parameters": {')[0].tolist()


    # chercher les parameter
    for i in range(len(ft_list)):
        if ft_list[i]['name'] == 'fn_add_numbers':
            parameter = ft_list[i]['parameters']
            # definition = ft_list[i]
            break

    # print(parameter)
    type_parameter = [i for i in parameter]

    print(f"merde on en est la {len(type_parameter)}")
    for i in range(len(type_parameter)):
        print(type_parameter[i])
        tokens += model.encode(f'"{type_parameter[i]}":')[0].tolist()
        txt += model.encode(f'"{type_parameter[i]}": ')[0].tolist()
        # tokens, txt = search_variable_number(tokens, txt, constraint['number'])
        tokens, txt = search_variable_number(tokens, txt, None)
        try:
            return json.loads(model.decode(txt))
        except Exception:
            ...

        if i < len(type_parameter):
            y = model.encode(f', ')[0].tolist()
            tokens += y
            txt += y


    return json.loads(model.decode(txt))

if __name__ == '__main__':
    with open("src/function_calling_tests.json", "r") as test_file:
        data = json.load(test_file)

    d = []
    for i in data:
        i.update(main(i['prompt']))
        print(i)
        d.append(i)

    print(d)

    with open("harimino.txt", "w") as f:
        f.write(d)
    # main("What is the sum of 265 and -345?")