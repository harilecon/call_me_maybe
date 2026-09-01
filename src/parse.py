from typing import TypedDict
import argparse


class ParseResult(TypedDict):
    functions_definition: str
    input: str
    output: str
    llm: str


def parse_input() -> ParseResult:
    parse = argparse.ArgumentParser()

    parse.add_argument(
        '-functions_definition',
        type=str,
        default='data/input/functions_definition.json',
        help="path to the list of functon definition"
        )

    parse.add_argument(
        '-input',
        type=str,
        default='data/input/function_calling_tests.json',
        help='path to function file'
    )

    parse.add_argument(
        '-output',
        type=str,
        default='output/function_calling_results',
        help='paht the output file'
    )

    parse.add_argument(
        '-llm',
        type=str,
        default="Qwen/Qwen3-0.6B",
        help='model with what you want to test'
    )

    argument = parse.parse_args()

    return {
        'functions_definition': argument.functions_definition,
        'input': argument.input,
        'output': argument.output,
        'llm': argument.llm
            }


if __name__ == '__main__':
    print(parse_input())
