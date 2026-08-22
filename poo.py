
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

    def _set_constraint_name(self) -> None:
        all_token_name = [x for ft in self.ft_list for x in self.model.encode(ft['name'])[0].tolist()]
        self._constraint_name = list(set(all_token_name))
        self._constraint_name.append(self.model.encode('"')[0].tolist()[0])
        return self._constraint_name


    def set_prompt(self, prompt: str) -> None:
        exemple = '{"name": "fn_add_numbers","parameters": {"a": 2.0, "b": 3.5}}'
        prompt = f"""
        Your task is to select the appropriate function from the available functions
        and extract its arguments from the user's request.
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

    # def _append_new_token(self, new_token: list[int]):
    #         self.output += new_token
    #         self._prompt += new_token         


    def search_name(self):
            for _ in range(10):
                ids = self.model.get_logits_from_input_ids(self._prompt)
                # print(self._constraint_name)
                self.mask_token(ids, self._constraint_name)
                next = ids.index(max(ids))
                self.output.append(next)
                self._prompt.append(next)
                # self._append_new_token(list[next])

                try:
                    output = self.model.decode(self.output)
                    json.loads(output)
                    break
                except Exception:
                    ...

                if next == self.model.encode('"')[0].tolist()[0]:
                    name = output.split('"')[3]
                    if name not in self.list_name:
                        return None

                    return name


    def search_parameter(self, constraint: list[int]):

        for _ in range(100):
            ids = self.model.get_logits_from_input_ids(self._prompt)
            if constraint:
                self.mask_token(ids, constraint)
    
            next = ids.index(max(ids))
            if next == 11:
                return None

            self._prompt.append(next)
            self.output.append(next)
            try:
                output = self.model.decode(self.output)
                print("dans la matrice")
                print(output)
                return(json.loads(output))
            except Exception:
                ...

        raise ValueError("reach max tokens")
            


    
    def solution(self):


        self._prompt += self.model.encode('{"name": "')[0].tolist()
        self.output += self.model.encode('{"name": "')[0].tolist()
        name = self.search_name()


        for definition in self.ft_list:
            if definition['name'] == name:
                def_selected = definition

        parameter = self.model.encode(', "parameters": {')[0].tolist()
        self._prompt += parameter
        self.output += parameter

        with open(self.model.get_path_to_vocab_file(), "r") as f:
            vocab = json.load(f)

        constraint = {
                'string': None,
                # 'number': [self.llm_vocabulary[i] for i in self.llm_vocabular if re.search("^[0-9\-\+.\,}\"]$" ,i)]
        'number': [vocab[i] for i in vocab if re.search("^[0-9\-\+.\,}]$" ,i)]
                
                }
        variable = def_selected['parameters'].keys()
        variable_len = len(variable)
        i = 0
        for key in def_selected['parameters'].keys():
            print(def_selected['parameters'][i])
            types = def_selected['parameters'][key]
            k = types.get('type')
            y = self.model.encode(f'"{k}":')[0].tolist()
            self._prompt += y
            self.output += y

            try:
                output = self.search_parameter(constraint[k])
                if output:
                    print("vita teto")
                    print(output)
                    print("vita teto")
                    sys.exit(0)
            except Exception as e:
                print(e)
                sys.exit(-1)
            if i < variable_len:
                i+=1
                y = self.model.encode(f', ')[0].tolist()
                self._prompt += y
                self.output += y


        # print(key)
        # print(self.model.decode(self.output))
        # print('TAPITRA')


            # definition = ft_list[i]

        # try:
        #     self.search_parameter(constraint[])





def main():
    call_me = CallMeMaybe()
    call_me.set_prompt("what is the sum of 3 and 4?")
    call_me.solution()





if __name__ == '__main__':
    main()