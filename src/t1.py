#!/usr/bin/env python
"""Demo callin ollama from litellm."""
# https://docs.litellm.ai/docs/providers/ollama

from litellm import completion

specs = [
        ("ollama/llama2", {}),
        ("ollama/llama2", {}),
        ("ollama/llama2", {"api_base":"http://localhost:11434"}),
        ("mistral/mistral-medium-latest", {}),
        ("openai/gpt-3.5-turbo", {}),
        ]

for (model, kwargs) in specs:
    print("----")
    print(f"{model}::::{api_base}")
    response = completion(
        messages=[{ "content": "respond in 20 words. who are you?","role": "user"}],
        model=model,
        **kwargs,
    )
    print(response.choices[0].message.content)

