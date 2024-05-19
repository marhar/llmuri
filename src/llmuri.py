#!/usr/bin/env python
"""
llmuri -- URI parsing for LLMs
"""

from urllib.parse import urlparse, parse_qs
from devtools import pprint
from typing import Dict, Tuple

api_abbreviations = {
    #TODO figure out how to specify e.g. openai protocol on localhost
    'mistralai': ('JUNK', 'https://api.mistral.ai/v1'),
    'openai': ('JUNK', 'https://api.openai.com/v1'),
    'claude': ('JUNK', 'https://api.anthropic.com/v1'),
    'ollama': ('JUNK', 'http://localhost:11434'),
}

api_special_litellm_cases = {
    'mistralai',
}

def uri_to_litellm(uri: str, verbose: bool = False) -> Dict[str, str]:
    """Returns a dict sutiable for passing to litellm."""

    rv = {}

    if not uri.startswith('llm://'):
        uri = 'llm://' + uri

    # We skip these parsed elements: fragments, params, username, password
    p = urlparse(uri, allow_fragments=False)

    # netloc look like: api_spec@api_base
    # If there is no @, then api_spec is the whole netloc

    netloc_parts = p.netloc.split('@')
    if len(netloc_parts) == 2:
        api_spec, api_base = netloc_parts
    else:
        api_spec = p.netloc
        api_base = None

    if api_spec in api_abbreviations:
        api_spec, api_base = api_abbreviations[api_spec]

    if api_base:
        rv['api_base'] = api_base

    model = p.path
    # get rid of leading / in path
    if model.startswith('/'):
        model = model[1:]

    rv['model'] = model
    query_dict = parse_qs(p.query)
    query_dict = {k: v[0] if len(v) == 1 else v for k, v in query_dict.items()}
    rv.update(query_dict)
    return rv


def tryone(uri):
    print("-" * 80)
    from litellm import completion

    print("uri:", uri)
    k = uri_to_litellm(uri)
    pprint(k)
    try:
        response = completion(
            messages=[{ "content": "respond in 20 words. who are you?","role": "user"}],
            **k
        )
        rid = response['id']
    except Exception as e:
        print("ERROR:", e)
        response = None
        rid = '******************************** ERROR ********************************'

    print(rid)


def xbatch(description, xs): pass
def batch(description, xs):
    print("batch:",description)
    for x in xs:
        tryone(x)


batch('nouri', [
"mistralai/mistral-medium",
"llm://mistralai/mistral-medium",
])

batch('abbreviations', [
"mistralai/mistral-medium",
#"@mistral.ai/mistral-medium",
#"@mistral.ai:80/mistral-medium",
"mistralai@mistral.ai:80/mistral-medium",
#"mistralai.v1@mistral.ai:80/mistral-medium",
#"api.mistral.ai.v1@mistral.ai:80/mistral-medium",
])

# anything before @ is api_spec
# anything after @ is api_base
# if there is an api_spec, pass that to litellm as api_spec

xbatch('query', [
"mistralai/mistral-medium",
"mistralai/mistral-medium?",
"mistralai/mistral-medium?temperature=0.2",
"mistralai/mistral-medium?max_tokens=4",
"mistralai/mistral-medium?temperature=0.2&max_tokens=4",
#ERROR "mistralai/mistral-medium?unsupported_option=12",
])

batch('fragments', [
"mistralai/mistral-medium",
#ERROR "mistralai/mistral-medium#",
#ERROR "mistralai/mistral-medium#fragment_that_should_be_ignored",
])

batch('abbreviations', [
"mistralai/mistral-medium",
"openai/gpt-4",
#"claude/claude-3-opus-20240229",  # TODO: get key
# "ollama/llama2",    # TODO: set provider
])

# TODO: break out tests as proper unit tests
# TODO: break out ERROR tests as proper unit tests
# TODO: fix add ollama provider
