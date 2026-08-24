from llm_sdk import Small_LLM_Model
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
            # print(x)
            json.loads(x)
            # print("\n\n\n\n\n\n\n\n")
            break
        except Exception:
            ...
        
    return (token, output_token)


def search_name(
    token,
    output_token: list[int],
    constraint,
    tab_name_tokenised: list[list[int]],
):
    tab = tab_name_tokenised.copy()

    for index in range(10):
        ids = model.get_logits_from_input_ids(token)

        mask_token(ids, constraint)

        next_token = ids.index(max(ids))

        # Le LLM a réellement généré ce token
        token.append(next_token)
        output_token.append(next_token)

        # On garde uniquement les noms compatibles
        tmp = []

        for name_tokenised in tab:
            if (
                index < len(name_tokenised)
                and name_tokenised[index] == next_token
            ):
                tmp.append(name_tokenised)

        tab = tmp

        # Aucun nom ne correspond
        if not tab:
            return None

        # Une seule fonction est identifiée
        if len(tab) == 1:
            remaining = tab[0][index + 1:]

            token.extend(remaining)
            output_token.extend(remaining)
            put_value(output_token, token, "\" ")
            return token, output_token

        # Token de fin
        if next_token == 1:
            return None

    return None

def select_function(function_name: str, ft_list: list) -> list[str]:
    for i in range(len(ft_list)):
        if ft_list[i]['name'] == function_name:
            return ft_list[i]



model = Small_LLM_Model("HuggingFaceTB/SmolLM2-1.7B-Instruct")
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

        with open("functions_definition.json", "r") as f:
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

    table_name_tokenised = [model.encode(ft['name'])[0].tolist() for ft in ft_list]

    name = list(set([x for ft in ft_list for x in model.encode(ft['name'])[0].tolist()]))
    name.append(model.encode("\"")[0].tolist()[0])


    output_token = []
    token = model.encode(prompt)[0].tolist()





    put_value(output_token, token, '{"name": "')



    token, output_token =  search_name(token, output_token, name, table_name_tokenised)
    # print(model.decode(output_token))
    # sys.exit(1)




    function_name = model.decode(output_token).split("\"")[3]

    put_value(output_token, token, ', "parameters": {')



    constraint = {
        'string': None,
        'number': [vocab[i] for i in vocab if re.search("^[0-9\-\+.\,\"Ġ]$" ,i)]
        }





    function_selected = select_function(function_name, ft_list)
    parameter = function_selected['parameters']
    type_parameter = [i for i in parameter]


    for i in range(len(type_parameter)):
        types = function_selected['parameters'][type_parameter[i]]['type'] 

        put_value(output_token, token, f'"{type_parameter[i]}":')


        token, output_token = search_variable_number(token, output_token, constraint[types])
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
    with open("function_calling_tests.json", "r") as test_file:
        data = json.load(test_file)

    d = []
    for i in data:
        i.update(main(i['prompt']))
        print(i)
        d.append(i)

    print(d)

    with open("harimino.output_token", "w") as f:
        f.write(str(d))
