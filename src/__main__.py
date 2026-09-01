from .call import call_me_maybe
import json
from .parse import parse_input
from .validation_model import MyFuctionDefinition, MyFunctionCall
from pydantic import ValidationError
import sys
from llm_sdk import Small_LLM_Model


def call_me():
    try:
        argument = parse_input()
        try:
            with open(argument['functions_definition'], 'r') as f:
                functions_definition = json.load(f)

            for function in functions_definition:
                MyFuctionDefinition(**function)
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
            print("error with the module llm_Sdk")
            print(e)
            sys.exit(-1)

        for prompt in prompt_file:
            try:
                prompt.update(
                    call_me_maybe(
                        prompt['prompt'],
                        functions_definition,
                        model
                        )
                    )
                validate = MyFunctionCall(**prompt)
            except ValidationError as e:
                print("error on validation of the returned function call")
                print(f"prompt = \"{prompt}\"")
                print("got from the llm:")
                print(prompt)
                print(e)
            prompt.update(validate)
            final.append(prompt)
            print(json.dumps(str(prompt), indent=2))
            print("\n\n")
        print(final)
    except Exception as e:
        print(e)
        sys.exit(-1)


if __name__ == '__main__':
    try:
        call_me()
    except KeyboardInterrupt:
        print("your are the boss")
