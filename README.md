*This project has been created as part of the 42 curriculum by <b>tsitoand</b>*

> ... Hey, I just met you, and this is crazy
But here's my number, so
# call me maybe

### Description
A function call is the code or instruction that tells a computer program or an AI model to run a specific routine, tool, or API. In AI, it lets a language model output structured data to trigger external actions rather than just generating text .

To perform this project whe have to master constraint decoding to force the LLM to produce JSON valid file. For this project whe use Qwen/Qwen3-0.6B

### Instructions

## Install LLM SDK

```shell
uv sync
```
## Install depandecy
```shell
uv 
```
## using Makefile
* install
```shell
make install
```
* run
```shell
make run
```

### Resources


AI was use to generate prompt

genrate test test

### Algorithm explanation
In Large Language Models (LLMs), Finite State Machines (FSMs) are used to enforce structural rules on text generation. This process is called <b>Structured Generation</b> or <b>Guided Decoding</b>.
<h1>How It Works</h3> 

* States: Represent the current position in a specific syntax or pattern (e.g., inside a JSON object, reading a key, reading a string)

* <b> Inputs:</b> The next potential tokens predicted by the LLM.Transitions: Valid legal characters allowed next by the schema rules.

* <b>Logit Bias / Masking:</b> The FSM blocks invalid transition tokens by setting their mathematical probability to zero (-inf). The LLM is forced to pick only from valid tokens.

### Design decisions
For this project i preferd to fixe the Json value structur to enforce the LLM to avoid wasting ressource on generating tokens. So the LLM have just to genereta the function name an choice the parameter from the prompt
### Performance analysis

### Challenges faced

### Testing strategy

### Example usage

#### Tested on :
* Qwen/Qwen3-0.6B
* Qwen/Qwen3-1.7B
* HuggingFaceTB/SmolLM2-1.7B-Instruct
* uggingFaceTB/SmolLM2-360M-Instruct


#### other LLM 
* tiiuae/Falcon3-1B-Instruct
* tiiuae/Falcon3-3B-Instruct
* microsoft/Phi-3.5-mini-instruct
* microsoft/Phi-4-mini-instruct
* ibm-granite/granite-3.3-2b-instruct
* ibm-granite/granite-3.3-8b-instruct
* TinyLlama/TinyLlama-1.1B-Chat-v1.0
* TinyLlama/TinyLlama-1.1B-Chat-v1.0
* apple/OpenELM-270M-Instruct
* apple/OpenELM-450M-Instruct
* apple/OpenELM-1_1B-Instruct
* stabilityai/stablelm-2-1_6b-chat
* mistralai/Ministral-8B-Instruct-2410