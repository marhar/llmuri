# llmuri -- URI support for LLMs

This project defines a standard URI for specifying LLMs and provides functionality to
convert LLM strings for use with popular LLM packages.

# Example

```
from llmuri import uri_to_litellm
from litellm import completion

for uri in [
    "llm:openai/gpt-4",
    "openai/gpt-4",
    "llm:ollama/llama2",
    "llm:mistralai/mistral-medium?temperature=0.2&max_tokens=4",
    "llm:ollama@example.com:11434/llama2",
]:
    kwargs = uri_to_litellm(uri)
    response = completion(
        messages=[{"content": "respond in 20 words. who are you?", "role": "user"}],
        **kwargs,
    )
    print(response)
```

## Installation

```
pip install llmuri
```

## URI Specification

[*scheme*:]*api-spec*[@*host*[:*port*]]/*model-name[?*parameter1*=*value1*[&*parameter2*=*value2*]...

examples:

```
ollama/llama2
llm:ollama/llama2?temperature=0.2
llms:ollama@example.com:11434/llama2
```

- *scheme* can be "llm" or "llms" to specify that the LLM is hosted behind
  an https web service.  If the scheme is ommitted, "llm" is assumed.

- *api-spec* is the name of the LLM service.

- *host* is an optional hostname where the LLM service is located.

- *port* is the service's port number.

- *model-name* is the name of the model to be executed.

- *parameter-list* is a list of model-specific parameters.
