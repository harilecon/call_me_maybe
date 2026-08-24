*This project has been created as part of the 42 curriculum by <b>tsitoand</b>*

### Description

### Instructions

### Resources

### Algorithm explanation

### Design decisions

### Performance analysis

### Challenges faced

### Testing strategy

### Example usage

Tested on :
* Qwen/Qwen3-0.6B
* Qwen/Qwen3-1.7B
* HuggingFaceTB/SmolLM2-1.7B-Instruct
* uggingFaceTB/SmolLM2-360M-Instruct

to test later

model_name = "tiiuae/Falcon3-1B-Instruct"
model_name = "tiiuae/Falcon3-3B-Instruct"
model_name = "microsoft/Phi-3.5-mini-instruct"
model_name = "microsoft/Phi-4-mini-instruct"
model_name = "ibm-granite/granite-3.3-2b-instruct"
model_name = "ibm-granite/granite-3.3-8b-instruct"
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
model_name = "apple/OpenELM-270M-Instruct"
model_name = "apple/OpenELM-450M-Instruct"
model_name = "apple/OpenELM-1_1B-Instruct"
model_name = "stabilityai/stablelm-2-1_6b-chat"
model_name = "mistralai/Ministral-8B-Instruct-2410"



MODELS = [
    # Petit
    "google/gemma-3-270m",
    "apple/OpenELM-270M-Instruct",
    "HuggingFaceTB/SmolLM2-360M-Instruct",

    # ~1B
    "Qwen/Qwen3-0.6B",
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "apple/OpenELM-1_1B-Instruct",
    "tiiuae/Falcon3-1B-Instruct",

    # ~2B
    "Qwen/Qwen3-1.7B",
    "HuggingFaceTB/SmolLM2-1.7B-Instruct",
    "ibm-granite/granite-3.3-2b-instruct",

    # ~3B+
    "HuggingFaceTB/SmolLM3-3B",
    "microsoft/Phi-3.5-mini-instruct",
]