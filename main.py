from src.llm_sdk.llm_sdk import Small_LLM_Model
import sys
import json
import math
import re


def search_variable_number(token, output_token: list, constraint):

    for _ in range(100):
        ids = model.get_logits_from_input_ids(token)

        next = ids.index(max(ids))
        if next == 11:
            break
        if constraint:
            mask_token(ids, constraint)

        output_token.append(next)
        token.append(next)
        try:
            x = model.decode(output_token)
            print(x)
            json.loads(x)
            break
        except Exception:
            ...
        
    return (token, output_token)



def search_name(token, output_token: list, constraint):
    for _ in range(10):
        ids = model.get_logits_from_input_ids(token)


        mask_token(ids, constraint)
        next = ids.index(max(ids))
        token.append(next)
        output_token.append(next)
        try:
            x = model.decode(output_token)
            json.loads(x)
            break
        except Exception:
            ...

        if next == 1:
            break

        print(x)

    return (token, output_token)

def select_function(function_name: str, ft_list: list) -> list[str]:
    for i in range(len(ft_list)):
        if ft_list[i]['name'] == function_name:
            return ft_list[i]



model = Small_LLM_Model()
vocab = model.get_path_to_vocab_file()



def mask_token(ids: list[float], valid: list):
    for i in range(len(ids)):
        if i not in valid:
            ids[i] = -math.inf


def put_value(output_token: list[int],token: list[int], value: str) -> None:
    message_tokenised = model.encode(value)[0].tolist()
    output_token += message_tokenised
    token += message_tokenised


def main(msg):

    try:
        with open(model.get_path_to_vocab_file(), "r") as f:
            vocab = json.load(f)

        with open("src/functions_definition.json", "r") as f:
            ft_list: list[dict] = json.load(f)

    except Exception:
        print("Error")
        sys.exit(-1)


    ex = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.5}}'
    prompt = f"""
    Your task is to select the appropriate function from the available functions
    and extract its arguments from the user's request.
    Available functions: {ft_list}
    Example:
    User request: 'what's the sum of 2,0 and 3,5'
    Output: {ex}
    User request: {msg}
    Output: 
    """


    name = list(set([x for ft in ft_list for x in model.encode(ft['name'])[0].tolist()]))
    name.append(model.encode("\"")[0].tolist()[0])


    output_token = []
    token = model.encode(prompt)[0].tolist()





    put_value(output_token, token, '{"name": "')



    token, output_token =  search_name(token, output_token, name)




    function_name = model.decode(output_token).split("\"")[3]

    put_value(output_token, token, ', "parameters": {')



    constraint = {
        'string': None,
        'number': [vocab[i] for i in vocab if re.search("^[0-9\-\+.\,}\"Ġ]$" ,i)]
        }

    # output_token = '{"name": "fn_add_numbers", "parameters": {'
    # token += model.encode('{"name": "fn_add_numbers", "parameters": {')[0].tolist()


    # chercher les parameter




    function_selected = select_function(function_name, ft_list)
    parameter = function_selected['parameters']
    type_parameter = [i for i in parameter]


    for i in range(len(type_parameter)):
        types = function_selected['parameters'][type_parameter[i]]['type'] 

        put_value(output_token, token, f'"{type_parameter[i]}":')


        token, output_token = search_variable_number(token, output_token, constraint[function_selected['parameters'][type_parameter[i]]['type']])
        try:
            return json.loads(model.decode(output_token))
        except Exception:
            ...

        if i < len(type_parameter):
            y = model.encode(f', ')[0].tolist()
            token += y
            output_token += y


    return json.loads(model.decode(output_token))





















if __name__ == '__main__':
    with open("src/function_calling_tests.json", "r") as test_file:
        data = json.load(test_file)

    d = []
    for i in data:
        i.update(main(i['prompt']))
        print(i)
        d.append(i)

    print(d)

    with open("harimino.output_token", "w") as f:
        f.write(str(d))
    # main("What is the sum of 265 and -345?")