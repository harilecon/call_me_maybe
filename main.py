from src.llm_sdk.llm_sdk import Small_LLM_Model
import sys
import json
import math
import re


model = Small_LLM_Model()

def main(msg):

    with open("src/functions_definition.json", "r") as f:
        ft_list: list[dict] = json.load(f)





    print(model.get_path_to_vocab_file())

    name = []



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
    name += [1]



    def get_name(ids: list[float], valid: list):
        for i in range(len(ids)):
            if i not in valid:
                ids[i] = -math.inf


    template = '{"name": "'



    # recherche name

    tokens1  = model.encode(prompt)[0].tolist()
    tokens = tokens1
    tokens += model.encode(template)[0].tolist()

    txt = ""
    txt += template

    b = False


    with open("/home/tsitoand/Desktop/vocab.json", "r") as f:
        vocab = json.load(f)

    number = [i for i in vocab if re.search("^[0-9\-\+.\,}]$" ,i)]


    def test1(tokens, txt, constraint):
        # print("my test")
        # print(model.decode(constraint))
        # sys.exit(42)

        for _ in range(100):
            log = model.get_logits_from_input_ids(tokens)
            


            # if constraint:
            #     get_name(log, constraint)
            #     next = log.index(max(log))
            #     try:
            #         print("int vovertion")
            #         int(model.decode(next))
            #     except ValueError:
            #         print("error convertion")
            #         break
            #     finally:
            #         tokens.append(next)
            #         txt += model.decode(next)

            # else:
            next = log.index(max(log))
            tokens.append(next)
            x = model.decode(next)
            txt += x
            # k = 0
            # if "\"" in x:
            #     k+=1
            #     if k > 1:
            #         break


            if level_breaker(txt):
                print(txt)
                break

            # if next == 1:
            #     print("tapaka teto")
            #     b = True
            #     break

            print(txt)
            print("--------------------------------------")
        return (tokens, txt)


    def test(tokens, txt, constraint):
        for _ in range(10):
            log = model.get_logits_from_input_ids(tokens)
            # constrainte_name(log, name)


            get_name(log, constraint)
            next = log.index(max(log))
            tokens.append(next)
            txt += model.decode(next)
            if level_breaker(txt):
                break

            if next == 1:
                print("tapaka teto")
                b = True
                break

            print(txt)
            print("--------------------------------------")

        # else:
        #     print("Error infinite loop")
        #     # sys.exit(-1)

        return (tokens, txt)

    tokens, txt =  test(tokens, txt, name)
    # print(txt)
    
    if b:
        print(txt)


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
        print(txt)

        constraint = {
            'string': None,
            'number': [vocab[i] for i in vocab if re.search("^[0-9\-\+.\,}\"]$" ,i)]
            }

        tokens, txt = test1(tokens, txt, None)
        # for i in par:
        #     x = f'"{i}": '
        #     tokens += model.encode(x)[0].tolist()
        #     txt += x
        # #     break
        # # print(model.decode(tokens))
        #     # print(i, constraint[par[i]['type']])
        #     # sys.exit(44)
        #     tokens, txt = test1(tokens, txt, constraint[par[i]['type']])
        #     print(txt)
        # # tokens, txt = test(tokens, txt, name)
        return (json.loads(txt))


if __name__ == '__main__':
    with open("src/function_calling_tests.json", "r") as test_file:
        data = json.load(test_file)

    d = []
    for i in data:
        i.update(main(i['prompt']))
        d.append(i)

    print(d)