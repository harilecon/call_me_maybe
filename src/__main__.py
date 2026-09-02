"""_summary_."""
from typing import Any
from .call_me_maybe import call_me_maybe
from .parse_input_parameter import parse_input
from .validation_model import (MyFuctionDefinition,
                               MyFunctionCall,
                               ValidateParameter)
from pydantic import ValidationError
from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
import json
import sys
import os


def validate_fuction_definition(parameter: dict[str, Any]) -> None:
    first_validation = MyFuctionDefinition(**parameter).model_dump()
    if first_validation['parameters']:
        for value in first_validation['parameters']:
            ValidateParameter(**first_validation['parameters'][value])

        for value in first_validation['returns']:
            ValidateParameter(**first_validation['returns'])


def call_me() -> None:
    try:
        argument = parse_input()
        try:
            with open(argument['functions_definition'], 'r') as f:
                functions_definition = json.load(f)

            for function in functions_definition:
                validate_fuction_definition(function)
        except ValidationError:
            print("the following funtion definition is invalid")
            print(function)
            sys.exit(-1)

        try:
            with open(argument['input'], 'r') as f:
                prompt_file = json.load(f)
        except OSError as e:
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

    except Exception as e:
        print(e)
        sys.exit(-1)


if __name__ == '__main__':
    try:
        call_me()
    except KeyboardInterrupt:
        print("\nOk the boss")
