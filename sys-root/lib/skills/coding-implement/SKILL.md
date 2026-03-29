---
name: coding-implement
description: 在 OpenSpec 项目中，根据已完成的需求分析与工程结构设计，负责具体编码实现；当用户输入「编码实现」等指令时，结合 request-analysis 与 project-analysis 的输出，按分层编码规范自动生成或修改代码，并在需要时为新增数据表与对外服务生成对应的数据库与接口说明文档目录。
---

# 编码实现技能（coding-implement）

本技能用于在 OpenSpec 体系下承接「需求 → 工程结构」之后的**实际编码阶段**，使 AI 生成的代码：

- 与 `openspec/project.md` 中的项目宪法规范保持一致；
- 与 `project-rules/` 中的工程补充约束（命名、分层、数据模型、信息流、实现约束等）对齐；
- 与当前变更目录 `openspec/changes/[change-id]/` 下的 `proposal.md` / `design.md` / `specs/*` 要求一一对应；
- 必要时，为新增数据库表与对外服务生成 `info-database/` 与 `info-service-interface/` 下的元信息文档与脚本/说明。

**实现完成自检**：完成本轮编码与可选的信息文档更新后，须按本技能 **REFERENCE**《实现完成自检》执行自检，通过后再进入 code-review 或 func-test；详见 `agentsystem/skills/coding-implement/REFERENCE/实现完成自检.md`。

---

## 一、触发与前置依赖

- **触发指令示例**：
  - 「编码实现」
  - 「根据这个 change 开始写代码」
  - 「按当前方案生成接口实现/页面代码」

- **必须先完成的前置技能**：
  - `request-analysis`：已为本次需求（`change-id`）在 `docs/project-prd-changes/[change-id]/` 与 `openspec/changes/[change-id]/` 下产出前期方案、需求说明、变更提案与任务拆分。
  - `project-analysis`：已检查并在需要时更新 `openspec/project.md` 与 `project-rules/`，确保架构模式、技术栈、目录结构与命名约定明确。

- **前置资料来源（编码前需要主动阅读）**：
  - `openspec/changes/[change-id]/proposal.md`：理解本次变更的背景、目标与影响范围。
  - `openspec/changes/[change-id]/design.md`：了解具体技术与架构设计决策。
  - `openspec/changes/[change-id]/specs/*/spec.md`：逐条 Requirements + Scenarios 作为编码验收标准。
  - `openspec/project.md`：项目定位、架构模式、技术栈、目录结构、命名与格式约定。
  - `project-rules/`：分层架构规范、模块职责、命名规则、异常与日志规范、数据库与服务接口约束等。

---

## 二、总体工作流程

1. **锁定本次变更上下文（change-id）**
   - 从用户输入与现有上下文中确定当前工作的 `change-id`；若不明确，应主动向用户确认或从最近一次活跃的变更中选择。
   - 建议在编码阶段始终围绕**单一 change-id**，避免跨变更混写。

2. **对齐需求、结构与约定**
   - 结合 `request-analysis` / `project-analysis` 输出，完成以下对齐检查：
     - 每个将要实现的接口/页面/服务，对应到哪一条 `specs/*/spec.md` 中的 Requirement 与 Scenario；
     - 所使用的目录与文件命名是否符合 `openspec/project.md` + `project-rules/` 中的约定；
     - 若发现规范缺失或冲突，应暂停编码，提示是否需先更新 `project-rules/` 或补充设计文档。

3. **选择合适的编码规范 spec**
   - 根据即将实现的内容类型，选择或组合 `coding-implement/REFERENCE/` 下的规范：
     - **前端实现**：如页面、组件、前端状态与交互逻辑 → 参见 `REFERENCE/spec-frontend.md`。
     - **后端/服务端实现**：如业务逻辑、应用服务、接口适配、数据访问等 → 参见：  
       - `REFERENCE/spec-backend-business.md`（业务层）  
       - `REFERENCE/spec-backend-application.md`（应用层）  
       - `REFERENCE/spec-backend-presentation.md`（表现层 / API 入口）  
       - `REFERENCE/spec-backend-data.md`（数据访问层 / 仓储）  
       - `REFERENCE/spec-backend-adapter.md`（适配层 / 外部接口与网关）  
       - `REFERENCE/spec-backend-service.md`（服务层 / 领域服务或跨模块服务）
   - 在生成代码前，应先依据对应 spec 明确：
     - 输入输出模型；
     - 依赖关系与调用链；
     - 错误处理、日志、监控与安全要求；
     - 与数据库表和对外接口的映射关系。

4. **编码实现与文件组织**
   - 在实际工程代码目录中（例如 `src/`、`theme/`、`app/` 等，按项目约定），根据分层规范创建或修改代码文件：
     - 遵守项目约定的目录结构与命名规则；
     - 按所选分层 spec 的职责边界划分类、函数与模块；
     - 为每项 Requirement 最少实现一个可识别的代码单元（函数/方法/组件），并可在注释或提交信息中引用对应 Requirement ID。
   - 编码时应特别注意：
     - **不在错误的层次实现逻辑**（例如业务决策不应落在表现层、SQL 不应散落在业务层等）；
     - **不破坏 project-rules 中定义的边界**（例如不得跨越应用层直连数据层）；  
     - **可测试性**：代码结构应便于单元测试/集成测试，必要时在变更目录中补充测试任务。

5. **新增数据库表与对外服务的元信息管理**
   - 若本次变更涉及**新增或调整数据库表结构**：
     - 在项目根目录下创建或补充 `info-database/`：  
       - 为本次 change 创建对应子目录或文件（如 `info-database/[change-id]-tables.md`、`info-database/[change-id]-ddl.sql`）。  
       - 在 MD 文档中说明：表名、字段、索引、约束、与业务对象的映射关系以及变更原因。  
       - 在 DDL 脚本中给出可执行的建表/变更 SQL（如适用）。
   - 若本次变更涉及**新增或调整对外服务接口**（HTTP API、RPC、消息订阅等）：
     - 在项目根目录下创建或补充 `info-service-interface/`：  
       - 为本次 change 创建对应说明（如 `info-service-interface/[change-id]-api.md`）。  
       - 描述：接口目的、URL/Topic、方法、请求/响应结构、鉴权方式、错误码与幂等/重试策略等。  
   - 所有数据库与接口信息应与 `project-rules/` 中的数据模型与接口规范保持一致；如发现矛盾，需要回到结构设计阶段修正。

6. **回写进度与任务状态**
   - 编码完成后，应回到 `openspec/changes/[change-id]/tasks.md`：
     - 将已完成的编码任务打勾 `[x]`；
     - 如在编码过程中发现新增必要任务（如补充指标监控、补充边界测试等），应追加到任务列表中。
   - 如有必要，在 `design.md` 中记录关键实现取舍（例如选择何种缓存策略、事务边界设计、接口幂等实现方式等）。

---

## 三、与 OpenSpec 的对应关系

本技能处于「需求 → 结构 → 实现」链路的**实现阶段**，与 OpenSpec 各部分的关系如下：

- `openspec/project.md`：提供全局架构模式、技术栈与目录/命名约定，编码必须遵守。
- `project-rules/`：提供分层架构细则、模块边界、命名/日志/异常规范、数据与接口约束，是编码具体落地的直接参照。
- `openspec/changes/[change-id]/proposal.md`：说明本次变更的目的与影响，编码须确保不引入与声明范围不符的额外行为。
- `openspec/changes/[change-id]/design.md`：给出实现层面的关键决策，编码需与之对齐，若有变更应同步更新文档。
- `openspec/changes/[change-id]/specs/*/spec.md`：提供可验证的 Requirements + Scenarios，是编码与测试的验收清单。

---

## 四、与其他技能的协同方式

- **与 `request-analysis` 的关系**
  - `request-analysis` 负责将自然语言需求转化为结构化文档与 OpenSpec 变更目录，并完成任务拆分。
  - `coding-implement` 在此基础上，围绕任务清单逐项完成编码实现与相关元信息文档的生成。

- **与 `project-analysis` 的关系**
  - `project-analysis` 确保项目在工程结构层面的约定是统一且最新的。  
  - `coding-implement` 必须在其结果基础上进行编码；若在实现过程中发现结构与实现不一致，应提示是否回到 `project-analysis` 阶段进行调整。

- **与 `image-analysis` 的关系（前端场景）**
  - 对前端页面与交互，若已通过 `image-analysis` 提取布局与组件信息，`coding-implement` 应将这些结果转译为具体组件结构、样式与交互逻辑，实现时保持与视觉/交互稿一致。

---

## 五、执行时的注意事项

- **不越权修改结构性约定**  
  - 编码阶段不应随意改变已在 `project.md` 或 `project-rules/` 确立的架构模式与边界，如确有必要必须在设计与结构分析层先达成共识并更新文档。

- **保持实现与文档的双向一致性**  
  - 如在实现中对接口、数据模型或流程做了与设计不同的调整，需同步更新：
    - `design.md`；
    - 对应 `specs/*/spec.md` 中的 Requirements / Scenarios；
    - 必要时更新 `info-database/` 与 `info-service-interface/`。

- **遇到不确定项要主动提问**  
  - 对以下问题不得自行假设，应优先向用户确认：
    - 是否允许在当前 change 中引入新技术栈或基础设施；
    - 数据一致性、性能、可观测性、安全/合规等非功能性指标的具体要求；
    - 模糊的业务规则或边界条件。

- **关注可测试性与可维护性**
  - 代码结构应利于单元测试与集成测试，避免过长函数和高耦合模块；
  - 对关键路径应考虑日志、监控与告警的埋点位置，以便后续运维。

### 5.1 微信小程序代码约束（Reference）
- 本段为索引入口：当本次实现目标明确为微信小程序时，coding-implement 必须遵循 `coding-implement/REFERENCE/spec-wechat-miniprogram.md` 中的约束。

---

## 六、示例使用流程（某具体项目）

1. 用户输入：「编码实现：请根据 `add-mvp-health-food-theme` 的变更，完成主题首页推荐区与倒计时 Section 的代码实现」。  
2. AI（coding-implement）：
   1. 确认本次 change-id 为 `add-mvp-health-food-theme`，加载其 `proposal.md`、`design.md` 与 `specs/*/spec.md`。  
   2. 阅读 `openspec/project.md` 与 `project-rules/`，确认主题采用的架构模式、文件组织与命名约定。  
   3. 根据要实现的是前端 Section + 配置逻辑，选择 `spec-frontend.md` 与（如有）对应的后端配置/数据访问规范。  
   4. 在主题工程目录下创建或修改 Section 模板、Snippet、JS/CSS 等文件，按照分层与命名规范实现需求，并引用 Metafields/Settings 等数据源。  
   5. 若本次变更增加了新的统计记录表或对外统计接口，则在 `info-database/` 与 `info-service-interface/` 下为该 change 创建相应说明与 DDL/接口文档。  
   6. 更新 `tasks.md` 中相关任务为已完成，如有新增测试或监控任务则补充进去。

通过本技能配合 `request-analysis` 与 `project-analysis`，可以打通「需求 → 结构 → 实现」全链路，让编码实现始终服从 OpenSpec 体系下的文档与约定。

---

## 七、经验沉淀

> 详细经验见 [Memory: 质量门禁分层设计教训](file:///Users/billhu/agentsystem/sys-root/lib/memory/reflections/reflection-quality-gate-layer-design-lessons.md)

### 核心原则（按需读取Memory扩展）

1. **分层设计**：Layer1 (check_*.py) 管"是否使用LLM"，Layer2 (llm_enhancer) 管"Agent还是API"
2. **DRY原则**：共同逻辑抽象到 `llm_helper.py`
3. **Prompt传递**：Agent模式传路径，API模式传内容
4. **测试设计**：基于架构设计，分层独立验证

