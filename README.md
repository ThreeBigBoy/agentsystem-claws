# Agent DevClaw System（agentsystem）

> **产品版本**: v1.1.1 · **更新**: 2026-03-22  
> **一句话**：面向 **Cursor** 的 **多项目、可复用** AI 研发治理壳——**规则入口 + 可选 Python 门禁 + 按需技能/记忆库**，与业务代码 **仓库解耦**。

---

## 本仓是什么？

| 维度 | 说明 |
|------|------|
| **定位** | **不是**业务应用后端；**是**「怎么协作、先读谁、如何被门禁约束」的**治理内核**仓库。 |
| **系统层** | 宿主规则（`.cursor/rules/`）、`sys-root/lib/`（skills / memory / scripts）、`agents-md-enforcer` 等 **可执行能力**，全体项目共用。 |
| **用户层（当前）** | **`usr-devclaw/` = 「独立开发者」角色** 落点：`user.json`、`usr-rules/`（如 OpenSpec 流程、PROJECT-CONFIG）。其它角色（如股票研究员）**另设根目录**，演进中。 |
| **项目层** | 各业务 Git 仓库内 **`claw-config/`**、**`openspec/`**、**`src/`** 等；通过 **`workspace/{项目} → 业务仓 claw-config`** 软链挂载（目录名以实际仓库为准）。 |

详细分层、洋葱模型（L0–L5）、线框图与目录树示例见：**[docs/agentsystem-心智模型与框架设计说明书.md](./docs/agentsystem-心智模型与框架设计说明书.md)**。

---

## 能解决什么问题？

- **边界清晰**：系统能力 vs 用户侧 Agent 规则 vs 单仓交付物不混在一处。  
- **协作可重复**：多业务项目 **共用** 同一套内核与 `usr-rules`，避免每仓复制一套 OpenSpec 级流程。  
- **风险可拦截（可选）**：Python **门禁**在业务项目场景下可阻断「未按约定读 `AGENTS.md` / 配置」等操作（见 `sys-root/lib/scripts/agents-md-enforcer/`）。  
- **阅读成本可控**：`user.json` 集中 **跨项目阅读顺序**，`sys-root` **按需定点**打开，默认不通读全库。

---

## 如何应用？

### 最短路径（新成员）

1. **克隆本仓库**（`agentsystem`），用 Cursor 打开或与业务仓同工作区。  
2. **业务项目**侧维护 **`claw-config/`**（运行时）与 **`openspec/`**（治理）；源码在 **`src/`**（约定见 `usr-rules` / `openspec/project.md`）。  
3. **`workspace/`** 中为每个项目建 **软链** → 该仓库的 **`claw-config/`**（名称以仓库为准，如 `claw-config`）。  
4. **需要门禁时**：配置 `PYTHONPATH` 指向 `agents-md-enforcer`，对项目名执行 `quick_enforce("<项目键>")` 或 `enforcer.py`（详见下文「命令速查」）。  
5. **导航与偏好**：读 **`usr-devclaw/user.json`** 中的 `read_order_*`，再按需打开 `openspec`、单文件 skill/memory、`usr-rules`。

### 命令速查（门禁）

```bash
# 进入门禁目录后（或已配置 PYTHONPATH）
cd sys-root/lib/scripts/agents-md-enforcer
python3 enforcer.py <项目键>

# 一行验证（需 PYTHONPATH 含本目录）
python3 -c 'from agents_md_enforcer import quick_enforce; quick_enforce("<项目键>")'
```

依赖与更完整示例以本目录 **`README.md`**（enforcer）为准。

### 文档索引

| 文档 | 用途 |
|------|------|
| [docs/agentsystem-心智模型与框架设计说明书.md](./docs/agentsystem-心智模型与框架设计说明书.md) | 全局架构、分层、闭环、目录示例 |
| [docs/agentsystem-README-方案补充.md](./docs/agentsystem-README-方案补充.md) | README 详篇：Hybrid 示意、门禁与场景、FAQ、自定义（从旧 README 整理） |
| [docs/AGENTS-md-职责区分说明.md](./docs/AGENTS-md-职责区分说明.md) | `claw-config` vs `openspec` 职责 |
| [usr-devclaw/usr-rules/OpenSpec.md](./usr-devclaw/usr-rules/OpenSpec.md) | OpenSpec 流程（用户层条文） |
| [usr-devclaw/user.json](./usr-devclaw/user.json) | 阅读顺序与偏好 |

---

## 附录：产品版本更新日志

> 以下为 **本仓库产品/文档** 对外版本；与《心智模型与框架设计说明书》内部修订号对应关系见各条说明。

| 版本 | 日期 | 摘要 |
|------|------|------|
| **v1.1.1** | 2026-03-22 | 新增 **[docs/agentsystem-README-方案补充.md](./docs/agentsystem-README-方案补充.md)**：收录原 README 详版（Hybrid 示意、门禁与场景、FAQ、自定义等）。 |
| **v1.1.0** | 2026-03-22 | **README 重构**：正文精简为「是什么 / 解决什么 / 如何应用」；附录收录更新日志。同步心智模型文档至 **v1.8**（全局架构、用户层多角色、`usr-devclaw`=独立开发者、§1.4.1 目录结构示例）。 |
| **v1.0.0** | 2026-03-21 | 初版：**Hybrid** 思路（规则 + Python 门禁）、`agents-md-enforcer`、`workspace` 软链、`usr-devclaw/user.json` 等。 |

### 附：心智模型文档修订明细（与 v1.1.0 对齐）

| 文档版本 | 日期 | 说明（节选） |
|----------|------|----------------|
| 1.0 | 2026-03-22 | 初稿：分层、`user.json`、检查清单 |
| 1.1 | 2026-03-22 | 产品三层 vs 洋葱 L0–L5 |
| 1.2 | 2026-03-22 | `usr-rules` 归用户层；系统层 = 内核/工具 |
| 1.3 | 2026-03-22 | 线框图替代 Mermaid（后迭代为固定行宽版） |
| 1.4 | 2026-03-22 | 全局架构图：合流与读图说明 |
| 1.5 | 2026-03-22 | 多用户层 Agent 角色；项目 1:1 归属 |
| 1.6 | 2026-03-22 | 角色举例：独立开发者 / 股票研究员 |
| 1.7 | 2026-03-22 | **`usr-devclaw/` = 独立开发者** |
| 1.8 | 2026-03-22 | **§1.4.1** 目录结构示例 |

---

## 许可证

MIT License
