#!/usr/bin/env python3
import os, json, ssl, urllib.request, urllib.error
os.environ['SILICONFLOW_API_KEY'] = 'sk-hykeoxdjiozbswqeyjpzrcszoeddwnfudolpaewcgdeplesl'
os.environ['MINIMAX_API_KEY'] = 'sk-api-BfYM72ltHFHhz-OyiMDE7AqgHMoz-BsJdYVsQo24Nx_J7FqpcAh4q5gT-4LfX7EeYG-n768WwpfGY_nXLash0P34QC_UGLx0ZS4ga4nETE84qRTLxSc9e0A'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
with open('/Users/billhu/agentsystem/sys-root/config/models.json') as f:
    cfg = json.load(f)
for n, m in cfg['models'].items():
    print(f'测试 {n}...')
    try:
        data = json.dumps({'model': m['model_id'], 'messages': [{'role': 'user', 'content': 'Hi'}], 'max_tokens': 10}).encode()
        req = urllib.request.Request(f"{m['base_url']}/chat/completions", data=data, headers={'Authorization': f"Bearer {os.environ[m['api_key_env']]}", 'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            print(f'  OK: {r.read().decode()[:100]}')
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.read().decode()[:80]}')
    except Exception as e:
        print(f'  Error: {str(e)[:80]}')
    print()
