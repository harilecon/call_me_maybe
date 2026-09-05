"""Entry point for the function call implementation.

This module contains all the components required to run the application.
"""

from typing import Any
from ._call_me_maybe import call_me_maybe
from ._parse_input_parameter import parse_input
from ._validation_model import (MyFuctionDefinition,
                                MyFunctionCall,
                                ValidateParameter)
from pydantic import ValidationError
from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
import json
import sys
import os


def _validate_fuction_definition(parameter: dict[str, Any]) -> None:

    first_validation = MyFuctionDefinition(**parameter).model_dump()
    if first_validation['parameters']:
        for value in first_validation['parameters']:
            ValidateParameter(**first_validation['parameters'][value])

        for value in first_validation['returns']:
            ValidateParameter(**first_validation['returns'])


def call_me() -> None:
    """Launch all instances and generate their responses.

    The generated responses are saved to the default output file
    ``data/output/name.json``.

    Returns:
        None.
    """
    # try:
    argument = parse_input()
    try:
        with open(argument['functions_definition'], 'r') as f:
            functions_definition = json.load(f)

        for function in functions_definition:
            _validate_fuction_definition(function)
    except ValidationError:
        print("the following funtion definition is invalid")
        print(json.dumps(function, indent=2))
        sys.exit(-1)

    try:
        with open(argument['input'], 'r') as f:
            prompt_file = json.load(f)
    except OSError as e:
        print("error on opening input file")
        print(e)
        sys.exit(-1)

    final = []
    try:
        model = Small_LLM_Model(model_name=argument['llm'])
    except Exception as e:
        print("error wit the module llm_Sdk")
        print(e)
        sys.exit(-1)

    for prompt in prompt_file:
        if not isinstance(prompt, dict):
            print("invalid entry must be a json with key \"prompt\"")
            print(prompt)
            continue

        if 'prompt' not in prompt:
            print("invalid entry must be a json with key \"prompt\"")
            print(prompt)
            continue

        if not isinstance(prompt['prompt'], str):
            print("invalid entry must be a json with key \"prompt\" \
and anstr as value")
            print(prompt)
            continue

        try:
            your_call = call_me_maybe(
                            prompt['prompt'],
                            functions_definition,
                            model
                            )

            if not your_call:
                print("error with this call")
                print(prompt)
                continue

            prompt.update(your_call)
            validate = MyFunctionCall(**prompt)
        except ValidationError as e:
            print("error on validation of the returned function call")
            print(f"prompt = \"{prompt}\"")
            print("got from the llm:")
            print(prompt)
            print(e)
        prompt.update(validate)
        final.append(prompt)
        print(json.dumps(prompt, indent=2))

    try:
        default = "data/output/function_calling_results.json"
        if default == argument['output']:
            if not os.path.exists("data/output"):
                os.mkdir("data/output")

        with open(argument['output'], 'w') as file:
            json.dump(final, file, indent=2)
    except OSError as e:
        print(e)

    # except Exception as e:
    #     print("another error unknow man")
    #     print(e)
    #     sys.exit(-1)


if __name__ == '__main__':
    try:
        call_me()
    except KeyboardInterrupt:
        print("\nOk the boss")
