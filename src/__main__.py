from .call import call_me_maybe
import json
from .parse import parse_input
from pydantic import BaseModel
# from validation_model import MyFuctionDefinition, MyFunctionCall
from pydantic import ValidationError, Field
from typing import Annotated
import sys

class MyFuctionDefinition(BaseModel):
    name: Annotated[str, Field(..., min_length=3)]
    description: Annotated[str, Field(..., min_length=10)]
    parameters: Annotated[dict | None, Field(default=None)]
    returns: Annotated[dict | None, Field(default=None)]


class MyFunctionCall(BaseModel):
    prompt: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    parameters: Annotated[dict | None, Field(...)]

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
            print("explosssssion")
            print(e)
            sys.exit(-1)
        
        final = [] 
        
        for prompt in prompt_file:
            print("manomboka eto")
            print(call_me_maybe(prompt, functions_definition))
            print(final)
    except Exception as e:
        print("ary ato?")
        print(e)
        sys.exit(-1)
        
        
if __name__ == '__main__':
    call_me()