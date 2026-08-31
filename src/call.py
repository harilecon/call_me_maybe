from .validation_model import MyFuctionDefinition
from .parse import parse_input, ParseResult
from typing import Any
from llm_sdk import Small_LLM_Model
from pydantic import ValidationError
import sys
import json
import math


try:
    model = Small_LLM_Model()
except Exception as e:
    print(e)
    sys.exit(-1)


def _search_variable_number(
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

        try:
            x = model.decode(output_token)
            json.loads(x)
            break
        except Exception:
            ...

    return (token, output_token)


def _search_name(
    token: list[int],
    output_token: list[int],
    constraint: list[int],
    tab_name_tokenised: list[list[int]],
) -> tuple[list[int], list[int]] | None:
    tab = tab_name_tokenised.copy()

    for index in range(20):
        ids = model.get_logits_from_input_ids(token)

        _mask_token(ids, constraint)
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
            _put_value(output_token, token, "\" ")

            return (token, output_token)
    return None


def _select_function(
        function_name: str,
        ft_list: list[list[Any]]
        ) -> list[Any] | None:
    for i in range(len(ft_list)):
        if ft_list[i]['name'] == function_name:
            return ft_list[i]
    return None


def _mask_token(ids: list[float], valid: list) -> None:
    for i in range(len(ids)):
        if i not in valid:
            ids[i] = -math.inf


def _put_value(output_token: list[int], token: list[int], value: str) -> None:
    message_tokenised = model.encode(value)[0].tolist()
    output_token += message_tokenised
    token += message_tokenised


def call_me_maybe(
    msg: str,
    functions_definition: str
    ):
    try:
        ft_list = []
        with open(functions_definition, "r") as f:
            data = json.load(f)
            for ft in data:
                ft_list.append(MyFuctionDefinition(**ft).model_dump())

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

    exemple = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.5}}'
    prompt = f"""
    Select the appropriate function from the available functions
    and extract its arguments from the user's request.
    Available functions: {ft_list}
    Example:
    User request: 'what's the sum of 2,0 and 3,5'
    Output: {exemple}
    User request: {msg}
    Output:
    """

    table_name_tokenised = [
        model.encode(ft['name'])[0].tolist() for ft in ft_list
        ]
    name = [tok for name_tok in table_name_tokenised for tok in name_tok]
    name.append(model.encode("\"")[0].tolist()[0])

    output_token = []
    token = model.encode(prompt)[0].tolist()

    _put_value(output_token, token, '{"name": "')

    token, output_token = _search_name(
        token,
        output_token,
        name,
        table_name_tokenised
        )
    function_name = model.decode(output_token).split("\"")[3]

    function_selected = _select_function(function_name, ft_list)
    parameter = function_selected['parameters']

    if not parameter:
        _put_value(output_token, token, ', "parameters": null}')
        print(model.decode(output_token))
        return json.loads(model.decode(output_token))

    type_parameter = [i for i in parameter]

    _put_value(output_token, token, ', "parameters": {')

    for i in range(len(type_parameter)):
        _put_value(output_token, token, f'"{type_parameter[i]}":')
        token, output_token = _search_variable_number(token, output_token)

        try:
            return json.loads(model.decode(output_token))
        except Exception:
            ...

        if i < len(type_parameter) - 1:
            y = model.encode(', ')[0].tolist()
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

    return model.decode(output_token)
