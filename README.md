# llmuri -- URI support for LLMs

This project defines a standard URI for specifying LLMs and provides functionality to
convert LLM strings for use with popular LLM packages.

# Example

```
from llmuri import uri_to_litellm
from litellm import completion

for uri in [
    "llm://openai/gpt-4",
    "openai/gpt-4",
    "llm://ollama/llama2",
    "llm://mistralai/mistral-medium?temperature=0.2&max_tokens=4",
    "llm://ollama@example.com:11434/llama2",
]:
    kwargs = uri_to_litellm(uri)
    response = completion(
        messages=[{"content": "respond in 20 words. who are you?", "role": "user"}],
        **kwargs,
    )
    print(response)

## Installation

```
pip install llmuri
```

## Specification

[llm://]{service\_spec}/{model\_name}[?{parameters...}]

- *service\_spec*: The host/port or other specification of the service location.  Short
  aliases are provided for well-known LLM services.

- *model\_name* is the name of the model to be executed.

- *parameters* are any optional parameters to be passed to the model.
