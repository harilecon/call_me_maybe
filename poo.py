
from llm_sdk import Small_LLM_Model
import sys
import json
import math
import re


class CallMeMaybe:
    def __init__(self):
        try:
            self.model = Small_LLM_Model()
            self.vocab: str = self.model.get_path_to_vocab_file()

            with open(self.model.get_path_to_vocab_file(), "r") as f:
                self.llm_vocabulary = json.load(f)

            with open("functions_definition.json", "r") as f:
                self.ft_list: list[dict] = json.load(f)
                self.list_name = [i['name'] for i in self.ft_list] 

        except Exception as e:
            print(e)
            sys.exit(-1)
        
        self._prompt: list[int] = []
        self._constraint_name: list[int] = self._set_constraint_name()
        self.output: list[int] = []
        self.separator = [self.llm_vocabulary[i] for i in self.llm_vocabulary if (i == "," or i == '",' or i == ')",')]

    def _set_constraint_name(self) -> None:
        all_token_name = [x for ft in self.ft_list for x in self.model.encode(ft['name'])[0].tolist()]
        self._constraint_name = list(set(all_token_name))
        self._constraint_name.append(self.model.encode('"')[0].tolist()[0])
        return self._constraint_name


    def set_prompt(self, prompt: str) -> None:
        exemple = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.5}}'
        prompt = f"""
        select the appropriate function from the available functions
        and extract its arguments from the user's request.
        always valid json
        Available functions:
        {self.ft_list}
        Example:
        User request: 'what's the sum of 2,0 and 3,5'
        Output: {exemple}
        User request: {prompt}
        Output: 
        """
        self._prompt = self.model.encode(prompt)[0].tolist()

    def mask_token(self, ids: list[float], valid: list):
        for i in range(len(ids)):
            if i not in valid:
                ids[i] = -math.inf

    def search_name(self):
            for _ in range(10):
                ids = self.model.get_logits_from_input_ids(self._prompt)

                self.mask_token(ids, self._constraint_name)
                next = ids.index(max(ids))
                self.output.append(next)
                self._prompt.append(next)

                try:
                    output = self.model.decode(self.output)
                    json.loads(output)
                    break
                except Exception:
                    ...

                if next == self.model.encode('"')[0].tolist()[0]:
                    name = output.split('"')[3]
                    if name not in self.list_name:
                        raise ValueError('fumction name not found')

                    return name

    def search_parameter(self, constraint: list[int]):

        for _ in range(100):
            ids = self.model.get_logits_from_input_ids(self._prompt)

            if constraint:
                self.mask_token(ids, constraint)
    
            next = ids.index(max(ids))
            if next in self.separator:
                if next == self.model.encode("')\",'")[0].tolist()[0]:
                    self.put_value(')')
                return None

            self._prompt.append(next)
            self.output.append(next)
            try:
                output = self.model.decode(self.output)
                return(json.loads(output))
            except Exception:
                ...

        raise ValueError("reach max tokens")

    def put_value(self, msg: str) -> None:
        msg_token = self.model.encode(msg)[0].tolist()
        self._prompt += msg_token
        self.output += msg_token

    def solution(self):
        self.put_value('{"name": "')

        name = self.search_name()

        for definition in self.ft_list:
            print(f"\n\n\n{name}\n\n\n")
            if definition['name'] == name:
                def_selected = definition

        self.put_value(', "parameters": {')

        with open(self.model.get_path_to_vocab_file(), "r") as f:
            vocab = json.load(f)

        constraint = {
                'string': None,
                'number': [vocab[i] for i in vocab if re.search("^[0-9\-.\,]$|^}}?$" ,i)]
                }
        variable = def_selected['parameters'].keys()
        variable_len = len(variable)
        i = 0
        for key in def_selected['parameters'].keys():

            types = def_selected['parameters'][key]
            k = types.get('type')

            self.put_value(f'"{key}":')

            try:
                output = self.search_parameter(constraint[k])
                if output:
                    self.output = []
                    return output

            except Exception as e:
                print(e)
                sys.exit(-1)
            if i < variable_len:
                i+=1
                if k == 'number':
                    self.put_value(', ')
                elif k == 'string':
                    self.put_value('",')

        # print(self.model.decode(self.output))


def main():
    with open("function_calling_tests.json", "r") as f:
        call = json.load(f)

    call_me: list[dict] = CallMeMaybe()
    tab = []

    for f in call:
        call_me.set_prompt(f)
        call_me.solution()
        f.update(call_me.solution())
        tab.append(f)
        print(f)

    print(tab)

    with open("harimino.txt", "w") as f:
        f.write(str(list(tab)))


if __name__ == '__main__':
    main()