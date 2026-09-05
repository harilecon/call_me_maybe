import json
import ast


test = '{"name": "fn_substitute_string_with_regex", "parameters": {"source_string": "programming", "regex": "(\w+)", "replacement": ""}}'

y = ast.literal_eval(test)
print(json.dumps(y))

