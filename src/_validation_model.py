from pydantic import BaseModel, Field
from typing import Annotated, Any
from enum import Enum


class AllowedValue(Enum):
    """Define the allowed values for function parameters."""

    NUMBER = 'number'
    NULL = None
    STRING = 'string'


class MyFuctionDefinition(BaseModel):
    """Define the structure of a function definition.

    Attributes:
        name: Name of the function. Must contain at least 3 characters.
        description: Description of the function. Must contain at least
            10 characters.
        parameters: Dictionary describing the function parameters, or None
            if the function does not require parameters.
        returns: Dictionary describing the function return value, or None
            if the function does not return a value.
    """

    name: Annotated[str, Field(..., min_length=3)]
    description: Annotated[str, Field(..., min_length=10)]
    parameters: Annotated[dict[str, Any] | None, Field(...)]
    returns: Annotated[dict[str, Any] | None, Field(...)]


class ValidateParameter(BaseModel):
    """Define the structure of a valid parameter.

    Attributes:
        type: allowed type of parameter value define on  AllowedValue
    """

    type: AllowedValue


class MyFunctionCall(BaseModel):
    """Define the structure of a function call.

    Attributes:
        prompt: User prompt used to generate the function call.
        name: Name of the function to call.
        parameters: Parameters to pass to the function, or None if the
            function does not require parameters.
    """

    prompt: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    parameters: Annotated[dict[str, Any] | None, Field(...)]
