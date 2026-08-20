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


    # def level_breaker(s: str) -> bool:
    #     l = 0

    #     for i in s:
    #         if i == '{':
    #             l += 1
    #         if i == '}':
    #             l -= 1
    #     if not s:
    #         return False
        
    #     if l == 0:
    #         print("our time as come")
    #         return True
    #     return False


    ft_name = [ft['name'] for ft in ft_list]


    name = [x for ft in ft_list for x in model.encode(ft['name'])[0].tolist()]
    name = list(set(name))
    name.append(1)
    name += [1]



    def get_name(ids: list[float], valid: list):
        for i in range(len(ids)):
            if i not in valid:
                ids[i] = -math.inf


    template = '{"name": "'



    # # # recherche name

    tokens1  = model.encode(prompt)[0].tolist()
    tokens = tokens1
    tokens += model.encode(template)[0].tolist()

    txt = ""
    txt += template

    b = False


    with open("/home/tsitoand/.cache/huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca/vocab.json", "r") as f:
        vocab = json.load(f)

    # number = [i for i in vocab if re.search("^[0-9\-\+.\,}]$" ,i)]


    def test1(tokens, txt, constraint):

        for _ in range(100):
            log = model.get_logits_from_input_ids(tokens)

            next = log.index(max(log))
            if next == 11:
                break

            get_name(log, constraint)

            tokens.append(next)
            x = model.decode(next)
            txt += x
            try:
                json.loads(txt)
                print(txt)
                break
            except Exception:
                ...

        return (tokens, txt)


    def test(tokens, txt, constraint):
        for _ in range(10):
            log = model.get_logits_from_input_ids(tokens)
            # constrainte_name(log, name)


            get_name(log, constraint)
            next = log.index(max(log))
            tokens.append(next)
            txt += model.decode(next)
            try:
                json.loads(txt)
                break
            except Exception:
                ...

            if next == 1:
                b = True
                break

            # print(txt)
            # print("--------------------------------------")

        return (tokens, txt)

    tokens, txt =  test(tokens, txt, name)
    # print(txt)
    
    # if b:
    #     # print(txt)


    n = txt.split("\"")[3]
    if n not in ft_name:
        print("invalide name")
        sys.exit(-2)

    else:
        print(f"found {n}")

        for j in ft_list:
            if j['name'] == n:
                x = j
        g = ', "parameters": {'

        tokens += model.encode(g)[0].tolist()
        txt += g

        par = x['parameters']
        # print(txt)

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
    x = [i for i in parameter]

    for i in range(len(x)):
        # print(definition['parameters'][i]['type'])
        tokens += model.encode(f'"{x[i]}": ')[0].tolist()
        txt += f'"{x[i]}": '
        tokens, txt = test1(tokens, txt, constraint['number'])
        if i < len(x):
            tokens += model.encode(f', ')[0].tolist()
            txt += f', '


    # for i in r
    # for i in par:
    #     x = f'"{i}": '
    #     tokens += model.encode(x)[0].tolist()
    #     txt += x
    #     #     break
    #     # print(model.decode(tokens))
    #         # print(i, constraint[par[i]['type']])
    #         # sys.exit(44)
    #     tokens, txt = test1(tokens, txt, constraint[par[i]['type']])
    # print(txt)
    print(model.decode(tokens))
    # sys.exit(0)
    #     # tokens, txt = test(tokens, txt, name)
    #     return (json.loads(txt))


if __name__ == '__main__':
    # with open("src/function_calling_tests.json", "r") as test_file:
    #     data = json.load(test_file)

    # d = []
    # for i in data:
    #     i.update(main(i['prompt']))
    #     d.append(i)

    # print(d)
    main("What is the sum of minus on thousend and -9635?")