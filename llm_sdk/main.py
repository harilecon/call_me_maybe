from llm_sdk import *


model = Small_LLM_Model(
    model_name="Qwen/Qwen3-0.6B"
)

prompt = "hello what your name?"

test = model.encode(prompt).tolist()[0]
next = model.get_logits_from_input_ids(test)
next.index(max)
print(model.decode())

