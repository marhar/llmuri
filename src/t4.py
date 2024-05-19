#!/usr/bin/env python
from urllib.parse import urlparse

parts="uri,scheme,netloc,path,params,query,fragment,username,password,hostname,port".split(',')
parts="uri,scheme,path,query".split(',')
import duckdb
duckdb.sql("""
create table t(
   uri text,
   scheme text,
   model text,
   query text,
   api_spec text,
   api_base text)
""")

api_abbreviations = {
    #TODO figure out how to specify e.g. openai protocol on localhost
    'mistralai': ('mistral-filler', 'https://api.mistral.ai/v1'),
    'openai': ('asdf', 'https://example.ai/v1'),
    'claude': ('asdf', 'https://example.ai/v1'),
}

api_special_litellm_cases = {
    'mistralai',
}

def doit(uri):
    #print(uri)
    if not uri.startswith('llm://'):
        uri = 'llm://' + uri
    p = urlparse(uri, allow_fragments=False)

    # We skip these elements:
    #     fragments
    #     params
    #     username
    #     password

    # We split netloc into:
    #     api_spec
    #     api_base

    netloc_parts = p.netloc.split('@')
    if len(netloc_parts) == 2:
        api_spec, api_base = netloc_parts
    else:
        api_spec = p.netloc
        api_base = ''

    if api_spec in api_abbreviations:
        api_spec, api_base = api_abbreviations[api_spec]

    model = p.path
    # get rid of leading / in path
    if model.startswith('/'):
        model = model[1:]

    duckdb.sql(f"""
    insert into t values('{uri}','{p.scheme}','{model}','{p.query}','{api_spec}','{api_base}')
        """)

def batch(description, xs):
    print(description)
    duckdb.sql('delete from t')
    for x in xs:
        doit(x)
    print(duckdb.sql('select * from t'))

def xbatch(description, xs): pass

xbatch('nouri', [
"mistralai/mistral-medium",
"llm://mistralai/mistral-medium",
])

batch('abbreviations', [
"mistralai/mname",
"@mistral.ai/mname",
"@mistral.ai:80/mname",
"mistralai@mistral.ai:80/mname",
"mistralai.v1@mistral.ai:80/mname",
"api.mistral.ai.v1@mistral.ai:80/mname",
])

# anything before @ is api_spec
# anything after @ is api_base
# if there is an api_spec, pass that to litellm as api_spec

batch('logins', [
"vvv/mname",
"a.com/mname",
"a.com:80/mname",
"@a.com/mname",
"@a.com:80/mname",
"vvv@mistral.ai:80/mname",
"vvv.v1@mistral.ai:80/mname",
"api.mistral.ai.v1@mistral.ai:80/mname",
])

xbatch('query', [
"mistralai/mname?",
"mistralai/mname?q=a",
"mistralai/mname?q=a&r=b",
"mistralai/mname?temperature=0.2&max_tokens=50",
])

xbatch('fragments', [
"mistralai/mname",
"mistralai/mname#",
"mistralai/mname#foo",
])

xbatch('first_ones', [
"openai/gpt-4",
"mistralai/mistral-medium",
"ollama/llama2",
])
