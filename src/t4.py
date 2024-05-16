#!/usr/bin/env python
from urllib.parse import urlparse

parts="uri,scheme,netloc,path,params,query,fragment,username,password,hostname,port".split(',')
parts="uri,scheme,netloc,path,query,hostname,port".split(',')
import duckdb
duckdb.sql("""
create table t(
   uri text,
   scheme text,
   netloc text,
   path text,
   query text,
   hostname text,
   port text)
""")

def doit(uri):
    #print(uri)
    if not uri.startswith('llm://'):
        uri = 'llm://' + uri
    p = urlparse(uri, allow_fragments=False)
    duckdb.sql(f"""
    insert into t values('{uri}','{p.scheme}','{p.netloc}','{p.path}','{p.query}','{p.hostname}','{p.port}')
        """)

def batch(description, xs):
    print(description)
    duckdb.sql('delete from t')
    for x in xs:
        doit(x)
    print(duckdb.sql('select * from t'))

batch('nouri', [
"mistralai/mistral-medium",
"llm://mistralai/mistral-medium",
])
batch('logins', [
"mistralai/mname",
"mistral.ai/mname",
"mistral.ai:80/mname",
"mistralai@mistral.ai:80/mname",
"mistralai.v1@mistral.ai:80/mname",
"api.mistral.ai.v1@mistral.ai:80/mname",
])

batch('query', [
"mistralai/mname?",
"mistralai/mname?q=a",
"mistralai/mname?q=a&r=b",
])

batch('fragments', [
"mistralai/mname",
"mistralai/mname#",
"mistralai/mname#foo",
])


