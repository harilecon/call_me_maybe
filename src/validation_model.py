from pydantic import BaseModel, Field
from typing import Annotated


class MyFuctionDefinition(BaseModel):
    name: Annotated[str, Field(...)]
    description: Annotated[str, Field(...)]
    parameters: Annotated[dict | None, Field(default=None)]
    returns: Annotated[dict | None, Field(default=None)]


class MyFunctionCall(BaseModel):
    prompt: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    parameters: Annotated[dict | None, Field(...)]
