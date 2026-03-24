# 环境变量与 `models.json` 的配合说明

`models.json` 里每个 **provider** 通过字段 **`env_api_key`** 声明：运行时从**同名环境变量**读取 API Key，避免把密钥写进 JSON。

## 0. 宿主内置模型（`defaults.source` = `host`）

当 **`defaults.source` 为 `host`**（且 **`provider` 为 `cursor`** 等 **`kind`: `host-builtin`**）时：

- **不需要**为「默认对话」配置 `OPENAI_API_KEY`；**不**走本文件中的 HTTP API。
- 实际推理由 **Cursor / VS Code 等宿主**的内置模型完成，具体模型以**宿主界面里选的模型**为准。
- 仅当某任务通过 **`aliases` / `routing`** 解析到 **`source`: `api`** 的 provider 时，才需要对应 **`.env`** 里的 Key。

若将 **`defaults`** 改为 **`defaults_presets.api_openai_mini`**（`source`: `api`），再按下面章节配置 `.env`。

## 1. 推荐：在本目录使用 `.env`（不入库）

1. 复制模板：

   ```bash
cd ~/agentsystem/sys-root/config
cp .env.example .env
```

2. 用编辑器打开 **`.env`**，把各 `KEY=` 右侧填成真实密钥（不要加引号，除非值里含空格；含 `#` 时注意转义或换行规则）。

3. **不要提交 `.env`**：仓库根目录 `.gitignore` 已忽略 `**/.env`，请只提交 `.env.example`。

## 2. 在终端里加载 `.env`（当前会话）

在 **zsh** 中可手动导出（简单场景）：

```bash
set -a
source ~/agentsystem/sys-root/config/.env
set +a
```

之后同一终端里启动的脚本/CLI 都能读到 `OPENAI_API_KEY` 等变量。

> 若 `.env` 含非 `KEY=value` 行，请保证为注释（以 `#` 开头），避免 `source` 报错。

## 3. 持久化到「登录即生效」（可选）

若希望**所有终端**默认带上这些变量，可把**非敏感**逻辑写在 `~/.zshrc`，或只对 key 使用：

```bash
# 不推荐把明文密钥直接写进 .zshrc；更安全：只 source .env 文件
# 在 ~/.zshrc 末尾追加一行（路径按你机器调整）：
# [ -f "$HOME/agentsystem/sys-root/config/.env" ] && set -a && source "$HOME/agentsystem/sys-root/config/.env" && set +a
```

更稳妥的做法是用 **macOS Keychain**、**1Password CLI** 或 CI 密钥管理，由启动脚本注入环境变量。

## 4. 与 `models.json` 的对应关系

| `models.json` 中的 `env_api_key` | `.env.example` 中的变量 |
|----------------------------------|-------------------------|
| `OPENAI_API_KEY` | `OPENAI_API_KEY` |
| `AZURE_OPENAI_API_KEY` | `AZURE_OPENAI_API_KEY` |
| `OLLAMA_API_KEY` | `OLLAMA_API_KEY`（本地 Ollama 常留空） |
| `CUSTOM_LLM_API_KEY` | `CUSTOM_LLM_API_KEY` |

新增 provider 时：在 **`models.json`** 里写 `env_api_key` 名称，再在 **`.env.example`** 增加同名占位行，并在本说明中补一行。

## 5. Python 脚本（可选）

若使用 `python-dotenv`，可在项目入口：

```python
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent / "config" / ".env")
```

需先 `pip install python-dotenv`（若你的 agentsystem 运行时采用该方式）。
