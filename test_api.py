#!/usr/bin/env python3
import os
import json
import ssl

os.chdir("/Users/billhu/agentsystem")
os.environ.setdefault("SILICONFLOW_API_KEY", "sk-hykeoxdjiozbswqeyjpzrcszoeddwnfudolpaewcgdeplesl")
os.environ.setdefault("MINIMAX_API_KEY", "sk-api-BfYM72ltHFHhz-OyiMDE7AqgHMoz-BsJdYVsQo24Nx_J7FqpcAh4q5gT-4LfX7EeYG-n768WwpfGY_nXLash0P34QC_UGLx0ZS4ga4nETE84qRTLxSc9e0A")

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

import urllib.request
import urllib.error

with open("sys-root/config/models.json") as f:
    config = json.load(f)

print("测试模型连通性...\n")

for name, model in config["models"].items():
    print(f"测试 {name} ({model['provider']})...")
    print(f"  URL: {model['base_url']}/chat/completions")
    print(f"  Model: {model['model_id']}")

    api_key = os.environ.get(model["api_key_env"])
    if not api_key:
        print(f"  ❌ API Key 未配置 ({model['api_key_env']})\n")
        continue

    try:
        data = {
            "model": model["model_id"],
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 10
        }

        req = urllib.request.Request(
            f"{model['base_url']}/chat/completions",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15, context=context) as resp:
            result = json.loads(resp.read())
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"  ✅ 成功! 响应: {content[:50]}...")
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP错误: {e.code} - {e.read().decode()[:100]}")
    except Exception as e:
        print(f"  ❌ 错误: {str(e)[:100]}")
    print()
