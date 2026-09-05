from ._validation_model import MyFuctionDefinition
from typing import Any
from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
from pydantic import ValidationError
import sys
import json
import math
import ast


def call_me_maybe(
        msg: str,
        functions_definition: Any,
        model: Small_LLM_Model
) -> Any:
    """Control interface that orchestrates the LLM parameters and execution.

    Args:
        msg: User prompt to process.
        functions_definition: Function definitions loaded from the JSON file.
        model: Utility class wrapping a lightweight Hugging Face causal
            language
            model for fast, low-memory experimentation.

    Returns:
        A dictionary containing the selected function name and its parameters.
    """
    def _search_variable(
            token: list[int],
            output_token: list[int],
            type_parameter: str,
            ) -> tuple[list[int], list[int]]:

        for _ in range(20):
            ids = model.get_logits_from_input_ids(token)

            next = ids.index(max(ids))

            if next == model.encode(",")[0].tolist()[0]:
                break

            elif next == model.encode("\",")[0].tolist()[0]:
                next = model.encode("\"")[0].tolist()[0]
                output_token.append(next)
                token.append(next)
                return (token, output_token)

            elif next == model.encode(")\",")[0].tolist()[0]:
                next = model.encode(")\"")[0].tolist()[0]
                output_token.append(next)
                token.append(next)
                return (token, output_token)

            output_token.append(next)
            token.append(next)

            try:
                x = model.decode(output_token)
                x = ast.literal_eval(x)
                json.dumps(x)
                return (token, output_token)

            except SyntaxError:
                ...

        if type_parameter == 'string':
            next = model.encode("\"")[0].tolist()[0]
            output_token.append(next)
            token.append(next)

        return (token, output_token)

    def _mask_token(ids: list[float], valid: list[int]) -> None:
        for i in range(len(ids)):
            if i not in valid:
                ids[i] = -math.inf

    def _search_name(
        token: list[int],
        output_token: list[int],
        constraint: list[int],
        tab_name_tokenised: list[list[int]],
    ) -> tuple[list[int], list[int]] | None:
        for _ in range(20):

            ids = model.get_logits_from_input_ids(token)

            _mask_token(ids, constraint)

            next = ids.index(max(ids))

            if next == model.encode("\"")[0].tolist()[0]:
                output_token.append(next)
                token.append(next)
                break

            output_token.append(next)
            token.append(next)
        return (token, output_token)

    def _select_function(
            function_name: str,
            ft_list: list[dict[str, Any]]
            ) -> dict[str, Any] | None:
        for i in range(len(ft_list)):
            my_fuction: dict[str, Any] = ft_list[i]
            if my_fuction['name'] == function_name:
                return ft_list[i]
        return None

    def _put_value(
            output_token: list[int],
            token: list[int],
            value: str
    ) -> None:
        message_tokenised = model.encode(value)[0].tolist()
        output_token += message_tokenised
        token += message_tokenised

    try:
        ft_list = []
        for ft in functions_definition:
            ft_list.append(MyFuctionDefinition(**ft).model_dump())

    except ValidationError as e:
        print("there is a invalid definition in the function definition file")
        print(e)
        sys.exit(-1)

    def set_prompt(msg: str, ft_list: list[int]) -> Any:

        ex = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.5}}'
        prompt = f"""
        Select the appropriate function from the available functions
        and extract its arguments from the user's request.
        Available functions: {ft_list}
        Example:
        User request: 'what's the sum of 2,0 and 3,5'
        Output: {ex}
        User request: {msg}
        Output:"""

        return model.encode(prompt)[0].tolist()

    table_name_tokenised = [
        model.encode(ft['name'])[0].tolist() for ft in ft_list
        ]
    name = [tok for name_tok in table_name_tokenised for tok in name_tok]
    name.append(model.encode("\"")[0].tolist()[0])

    output_token: list[int] = []
    token = set_prompt(msg, ft_list)

    _put_value(output_token, token, '{"name": "')

    name_found = _search_name(
        token,
        output_token,
        name,
        table_name_tokenised
        )

    if not name_found:
        print("error on name research")
        return None

    token, output_token = name_found

    function_name = model.decode(output_token).split("\"")[3]

    for i in ft_list:
        if i['name'] == function_name:
            break

    function_selected = _select_function(
        function_name,
        ft_list
        )
    if not function_selected:
        print("no function selected")
        return None

    parameter = function_selected['parameters']

    if not parameter:
        _put_value(output_token, token, ', "parameters": null}')
        return json.loads(model.decode(output_token))

    type_parameter = [i for i in parameter]

    _put_value(output_token, token, ', "parameters": {')

    for i in range(len(type_parameter)):

        _put_value(output_token, token, f'"{type_parameter[i]}":')
        token, output_token = _search_variable(
            token,
            output_token,
            parameter[type_parameter[0]]['type']
            )

        try:
            txt = ast.literal_eval(str(model.decode(output_token)))
            return json.loads(json.dumps(txt))

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
                txt = ast.literal_eval(model.decode(output_token))
                return json.loads(txt)
            except Exception:
                ...

    return json.loads(model.decode(output_token))
