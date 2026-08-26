from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, Field, ValidationError
from typing import Annotated
import sys
import json
import math
import re


class MyFuctionDefinition(BaseModel):
    name: Annotated[str, Field(...)]
    description: Annotated[str, Field(...)]
    parameters: Annotated[dict | None, Field(...)]
    returns: Annotated[dict | None, Field(...)]

class MyFunctionCall(BaseModel):
    prompt: Annotated[str, Field(..., ge=1)]
    name: Annotated[str, Field(...)] 
    parameters: Annotated[dict | None, Field(...)]


def search_parameter(
        token: list[int],
        output_token: list[int],
        ) -> tuple[list[int], list[int]]:

    for _ in range(100):
        ids = model.get_logits_from_input_ids(token)


        next = ids.index(max(ids))




        if next == model.encode(",")[0].tolist()[0]:
            break

        elif next == model.encode("\",")[0].tolist()[0]:
            next = model.encode("\"")[0].tolist()[0]
            output_token.append(next)
            token.append(next)
            break


        output_token.append(next)
        token.append(next)

        # print(model.decode(output_token))

        try:
            x = model.decode(output_token)
            json.loads(x)
            break
        except Exception:
            ...

    return (token, output_token)


def search_name(
    token,
    output_token: list[int],
    constraint,
    tab_name_tokenised: list[list[int]],
) -> tuple[list[int], list[int]]:
    tab = tab_name_tokenised.copy()

    for index in range(20):
        ids = model.get_logits_from_input_ids(token)

        mask_token(ids, constraint)
        next_token = ids.index(max(ids))

        token.append(next_token)
        output_token.append(next_token)

        tmp = []
        for name_tokenised in tab:
            if (
                index < len(name_tokenised)
                and name_tokenised[index] == next_token
            ):
                tmp.append(name_tokenised)

        tab = tmp

        if not tab:
            raise ValueError("No name found for the prompt")

        if len(tab) == 1:
            remaining = tab[0][index + 1:]

            token.extend(remaining)
            output_token.extend(remaining)
            put_value(output_token, token, "\" ")

            return token, output_token


def select_function(function_name: str, ft_list: list) -> list[str]:
    for i in range(len(ft_list)):
        if ft_list[i]['name'] == function_name:
            return ft_list[i]


try:
    model = Small_LLM_Model()
    vocab = model.get_path_to_vocab_file()
except Exception as e:
    print(e)
    sys.exit(-1)


def mask_token(ids: list[float], valid: list):
    for i in range(len(ids)):
        if i not in valid:
            ids[i] = -math.inf


def put_value(output_token: list[int],token: list[int], value: str) -> None:
    message_tokenised = model.encode(value)[0].tolist()
    output_token += message_tokenised
    token += message_tokenised

# from test import time_decorator



# @time_decorator
def call_me_maybe(msg):

    try:
        ft_list = []
        with open("functions_definition.json", "r") as test_file:
                data = json.load(test_file)
                for ft in data:
                    ft_list.append(MyFuctionDefinition(**ft).model_dump())

        with open(model.get_path_to_vocab_file(), "r") as f:
            vocab = json.load(f)

    except json.decoder.JSONDecodeError as e:
        print("error on Json convertion")
        print(e)
        sys.exit(-1)

    except OSError as e:
        print("error opening the file")
        print(e)
        sys.exit(-1)

    except ValidationError as e:
        print("Validation Error")
        print(e)
        sys.exit(-1)



    # except Exception as e:
    #     print("Error")
    #     print(e)
    #     sys.exit(-1)

    ex = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.5}}'
    prompt = f"""
    Select the appropriate function from the available functions
    and extract its arguments from the user's request.
    Available functions: {ft_list}
    Example:
    User request: 'what's the sum of 2,0 and 3,5'
    Output: {ex}
    User request: {msg}
    Output: 
    """

    table_name_tokenised = [model.encode(ft['name'])[0].tolist() for ft in ft_list]
    name = [tok for name_tok in table_name_tokenised for tok in name_tok]
    name.append(model.encode("\"")[0].tolist()[0])


    output_token = []
    token = model.encode(prompt)[0].tolist()

    put_value(output_token, token, '{"name": "')

    token, output_token =  search_name(token, output_token, name, table_name_tokenised)
    function_name = model.decode(output_token).split("\"")[3]


    function_selected = select_function(function_name, ft_list)
    parameter = function_selected['parameters']

    if not parameter:
        put_value(output_token, token, ', "parameters": null}')
        return json.dump(model.decode(output_token))

    key_parameter = [i for i in parameter]

    # print(f"\n\n\n\n\n{key_parameter}\n\n\n\n\n\n")

    put_value(output_token, token, ', "parameters": {')

    # print(len(key_parameter))
    i = 0
    for key in range(len(key_parameter)):

        put_value(output_token, token, f'"{key}":')

        token, output_token = search_parameter(token, output_token)

        # print(f"\n\n\n\n\n\n{model.decode(output_token)}\n\n\n\n\n\n\n")
        try:
            return json.loads(model.decode(output_token))
        except Exception:
            ...

        if i < len(key_parameter) - 1:
            # print(i)
            y = model.encode(f', ')[0].tolist()
            token += y
            output_token += y
        else:
            y = model.encode('}}')[0].tolist()
            token += y
            output_token += y
            try:
                return json.loads(model.decode(output_token))
            except Exception:
                ...
        i+=1


        # print(model.decode(output_token))
        # else:
        #     y = model.encode('}}')[0].tolist()
        #     token += y
        #     output_token += y
    return model.decode(output_token)
    # return json.loads(model.decode(output_token))


if __name__ == '__main__':
    # print(call_me_maybe("great Shrek"))
    with open("function_calling_tests.json", "r") as test_file:
        data = json.load(test_file)

    # d = []
    # print(call_me_maybe('Replace all numbers in "Hello 34 I\'m 233 years old" with NUMBERS'))
    for i in data:
        print(call_me_maybe(i['prompt']))
        print(i)
        # d.append(i)

    # print(d)
