---
id: pattern-pluggable-extension-architecture
title: 可插拔扩展架构（自动发现+注册+加载机制）
type: pattern
description: 通过自动发现、动态注册、配置化加载机制，实现新组件的快速接入，无需修改代码即可扩展系统能力
description_long: |
  解决系统扩展时"需要修改代码、重新部署、耦合度高"的问题。
  通过自动发现（扫描目录）、动态注册（解析配置）、配置化加载（运行时加载）的三层机制，
  实现真正的"可插拔"扩展能力。
applicable_projects:
  - agentsystem
  - "*"
tags:
  - 架构设计
  - 可扩展性
  - 插件化
  - 自动发现
  - 配置化
related:
  - pattern-systematic-technical-design-review
  - pattern-production-readiness-checklist
  - anti-pattern-framework-substitution-trap
created_by: 复盘-deepen-langgraph-v2-11-1-技术方案评审过程
created_date: 2026-03-18
version: 1.0
---

# 可插拔扩展架构（自动发现+注册+加载机制）

## 一句话定义

通过自动发现（扫描目录）、动态注册（解析配置）、配置化加载（运行时加载）的三层机制，实现新组件的快速接入，无需修改代码即可扩展系统能力。

## 问题背景

### 常见的系统扩展问题

```
┌─────────────────────────────────────────────────────────────┐
│                    常见的系统扩展问题                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  问题 1: 扩展需要修改代码                                      │
│  • 新增Agent需要修改invoker代码                                 │
│  • 新增Skill需要修改注册表                                       │
│  • 新增Memory需要修改硬编码关联                                  │
│                                                              │
│  问题 2: 需要重新部署                                          │
│  • 每次扩展都要发版                                             │
│  • 影响线上稳定性                                               │
│  • 扩展成本高                                                   │
│                                                              │
│  问题 3: 耦合度高                                               │
│  • 扩展组件与核心系统紧耦合                                      │
│  • 一个扩展影响整体                                              │
│  • 难以独立演进                                                  │
│                                                              │
│  问题 4: 扩展流程繁琐                                          │
│  • 需要修改多处代码                                              │
│  • 需要更新配置                                                  │
│  • 需要重启服务                                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 模式解决方案

### 三层扩展机制

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      可插拔扩展架构（三层机制）                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Layer 1: 自动发现（Auto Discovery）                                    │    │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │                                                                     │    │
│  │ 职责: 自动扫描指定目录，发现新组件                                       │    │
│  │                                                                     │    │
│  │ 实现:                                                                │    │
│  │ • AgentAutoDiscovery                                                 │    │
│  │   - 扫描 /agentsystem/agents/                               │    │
│  │   - 解析 agent.md 文件                                               │    │
│  │   - 提取 agent_id, name, role, skills, inputs, outputs               │    │
│  │                                                                     │    │
│  │ • SkillAutoDiscovery                                                 │    │
│  │   - 扫描 /agentsystem/skills/                               │    │
│  │   - 解析 SKILL.md 文件                                               │    │
│  │   - 提取 skill_id, name, trigger_words, inputs, outputs            │    │
│  │                                                                     │    │
│  │ • MemoryAutoDiscovery                                                │    │
│  │   - 扫描 /agentsystem/memory/                               │    │
│  │   - 解析 memory.md 文件                                              │    │
│  │   - 提取 memory_id, type, tags, related_memories, applicable_steps │    │
│  │                                                                     │    │
│  │ • ProjectRulesLoader                                                 │    │
│  │   - 扫描 project-rules/ 目录                                          │    │
│  │   - 加载项目特定规则                                                   │    │
│  │   - 合并到Agent输入                                                    │    │
│  │                                                                     │    │
│  │ 触发方式:                                                            │    │
│  │ • 定期扫描（每5分钟）                                                  │    │
│  │ • 启动时全量扫描                                                       │    │
│  │ • 手动触发扫描                                                        │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Layer 2: 动态注册（Dynamic Registration）                            │    │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │                                                                     │    │
│  │ 职责: 将发现的组件注册到系统中                                         │    │
│  │                                                                     │    │
│  │ 注册表:                                                              │    │
│  │ • AgentRegistry: {agent_id -> agent_config}                          │    │
│  │ • SkillRegistry: {skill_id -> skill_config}                          │    │
│  │ • MemoryRegistry: {memory_id -> memory_config}                       │    │
│  │ • RulesRegistry: {rule_id -> rule_content}                           │    │
│  │                                                                     │    │
│  │ 注册过程:                                                            │    │
│  │ 1. 验证配置合法性（schema验证）                                          │    │
│  │ 2. 检查唯一性（id不重复）                                               │    │
│  │ 3. 添加到注册表                                                         │    │
│  │ 4. 触发加载回调（如需要）                                                │    │
│  │ 5. 记录注册日志                                                        │    │
│  │                                                                     │    │
│  │ 热更新支持:                                                          │    │
│  │ • 新增: 自动注册                                                       │    │
│  │ • 修改: 自动更新                                                       │    │
│  │ • 删除: 自动注销（标记为deprecated）                                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    ↓                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │ Layer 3: 配置化加载（Configuration-driven Loading）                   │    │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │    │
│  │                                                                     │    │
│  │ 职责: 运行时根据配置加载和使用组件                                       │    │
│  │                                                                     │    │
│  │ 加载策略:                                                            │    │
│  │ • Agent加载                                                          │    │
│  │   - 根据change_id和task选择合适的Agent                                  │    │
│  │   - 从注册表获取Agent配置                                               │    │
│  │   - 组装输入参数                                                        │    │
│  │   - 执行调用                                                           │    │
│  │                                                                     │    │
│  │ • Skill加载                                                          │    │
│  │   - 根据用户输入匹配trigger_words                                      │    │
│  │   - 从注册表获取Skill配置                                               │    │
│  │   - 执行Skill逻辑                                                       │    │
│  │                                                                     │    │
│  │ • Memory加载                                                         │    │
│  │   - 根据当前step匹配applicable_steps                                   │    │
│  │   - 从注册表获取Memory配置                                              │    │
│  │   - 自动唤醒相关Memory                                                  │    │
│  │                                                                     │    │
│  │ • Rules加载                                                          │    │
│  │   - 从project-rules加载项目特定规则                                      │    │
│  │   - 合并到Agent输入                                                     │    │
│  │   - 优先级: 项目规则 > 全局规则                                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 组件配置规范

#### Agent配置（agent.md）

```yaml
---
agent:
  id: "product-manager"
  name: "产品经理 Agent"
  role: "PRODUCT_MANAGER"
  version: "1.0"
  skills:
    - request-analysis
    - prd-authoring
    - prd-review
  inputs:
    - proposal.md
    - user-requirements
  outputs:
    - PRD
    - 需求分析记录
  rules:
    - agentsystem/global-rules/skills-rules-for-agent.md
    - project-rules/项目特定规则.md
  trigger_words:
    - "需求分析"
    - "PRD"
    - "产品设计"
---
```

#### Skill配置（SKILL.md）

```yaml
---
skill:
  id: "request-analysis"
  name: "需求分析技能"
  version: "1.0"
  trigger_words:
    - "需求分析"
    - "分析需求"
    - "需求梳理"
  inputs:
    - proposal.md
    - user-interview
  outputs:
    - PRD
    - 需求分析报告
  executor: "PRODUCT_MANAGER"
  steps:
    - 读取proposal
    - 提取背景和目标
    - 分析影响范围
    - 识别风险
    - 生成PRD
---
```

#### Memory配置（memory.md）

```yaml
---
memory:
  id: "pattern-quality-gate"
  title: "质量门禁检查模式"
  type: "pattern"
  tags:
    - quality
    - gate
    - check
  applicable_steps:
    - step2_prd_review
    - step4_architecture_review
    - step7_func_test
  related_memories:
    - pattern-complete-quality-closed-loop
    - anti-pattern-skip-phase-before-completion
  applicable_projects:
    - "*"
---
```

### 实现代码示例

```python
# 自动发现基类
class AutoDiscovery(ABC):
    """自动发现基类"""
    
    def __init__(self, scan_root: str, scan_interval: int = 300):
        self.scan_root = Path(scan_root)
        self.scan_interval = scan_interval
        self._registry: Dict[str, dict] = {}
        self._last_scan_time = 0
    
    async def scan(self) -> Dict[str, dict]:
        """执行扫描，返回新发现的组件"""
        new_items = {}
        
        for config_file in self.scan_root.rglob(self.config_pattern):
            try:
                config = await self._parse_config(config_file)
                item_id = self._extract_id(config)
                
                if item_id not in self._registry:
                    self._registry[item_id] = config
                    new_items[item_id] = config
                    print(f"✅ 发现新{self.item_type}: {item_id}")
                    
            except Exception as e:
                print(f"⚠️ 解析失败 {config_file}: {e}")
        
        return new_items
    
    @abstractmethod
    async def _parse_config(self, config_file: Path) -> dict:
        """解析配置文件"""
        pass
    
    @abstractmethod
    def _extract_id(self, config: dict) -> str:
        """提取组件ID"""
        pass


# Agent自动发现
class AgentAutoDiscovery(AutoDiscovery):
    """Agent自动发现"""
    
    config_pattern = "**/agent.md"
    item_type = "Agent"
    
    async def _parse_config(self, config_file: Path) -> dict:
        """解析agent.md"""
        import yaml
        async with aiofiles.open(config_file, 'r') as f:
            content = await f.read()
        return yaml.safe_load(content)
    
    def _extract_id(self, config: dict) -> str:
        return config.get("agent", {}).get("id")


# Skill自动发现
class SkillAutoDiscovery(AutoDiscovery):
    """Skill自动发现"""
    
    config_pattern = "**/SKILL.md"
    item_type = "Skill"
    
    async def _parse_config(self, config_file: Path) -> dict:
        """解析SKILL.md"""
        import yaml
        async with aiofiles.open(config_file, 'r') as f:
            content = await f.read()
        return yaml.safe_load(content)
    
    def _extract_id(self, config: dict) -> str:
        return config.get("skill", {}).get("id")


# Memory自动发现
class MemoryAutoDiscovery(AutoDiscovery):
    """Memory自动发现"""
    
    config_pattern = "**/memory.md"
    item_type = "Memory"
    
    async def _parse_config(self, config_file: Path) -> dict:
        """解析memory.md（frontmatter）"""
        import yaml
        async with aiofiles.open(config_file, 'r') as f:
            content = await f.read()
        # 提取frontmatter
        if content.startswith('---'):
            _, frontmatter, _ = content.split('---', 2)
            return yaml.safe_load(frontmatter)
        return {}
    
    def _extract_id(self, config: dict) -> str:
        return config.get("id")


# 全局注册表
class ComponentRegistry:
    """组件注册表（单例）"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.agents = {}
            cls._instance.skills = {}
            cls._instance.memories = {}
        return cls._instance
    
    def register_agent(self, agent_id: str, config: dict):
        self.agents[agent_id] = config
    
    def register_skill(self, skill_id: str, config: dict):
        self.skills[skill_id] = config
    
    def register_memory(self, memory_id: str, config: dict):
        self.memories[memory_id] = config
    
    def get_agent(self, agent_id: str) -> Optional[dict]:
        return self.agents.get(agent_id)
    
    def get_skill(self, skill_id: str) -> Optional[dict]:
        return self.skills.get(skill_id)
    
    def get_memory(self, memory_id: str) -> Optional[dict]:
        return self.memories.get(memory_id)
```

### 扩展流程

```
新增Agent/Skill/Memory/Rule
    ↓
创建配置目录和文件
    ↓
自动发现（扫描目录）
    ↓
解析配置（验证合法性）
    ↓
动态注册（添加到注册表）
    ↓
配置化加载（运行时可用）
    ↓
无需重启，立即生效
```

## 实施建议

### 适用场景

| 场景 | 适用性 | 说明 |
|-----|-------|------|
| Agent系统 | 高 | 新Agent快速接入 |
| Skill系统 | 高 | 新Skill快速接入 |
| Memory系统 | 高 | 新Memory自动关联 |
| 规则引擎 | 高 | 项目规则动态加载 |
| 插件系统 | 高 | 插件化架构 |
| 配置中心 | 中 | 配置动态更新 |

### 实施步骤

1. **定义配置规范**: 为每种组件定义清晰的配置格式
2. **实现自动发现**: 实现扫描和解析逻辑
3. **实现动态注册**: 实现注册表和验证逻辑
4. **实现配置化加载**: 在运行时根据配置使用组件
5. **添加监控**: 监控新组件的注册和使用情况

### 注意事项

| 注意点 | 解决方案 |
|-------|---------|
| 配置合法性验证 | Schema验证，错误提示 |
| 重复注册处理 | ID唯一性检查 |
| 配置热更新 | 监听文件变化或定期扫描 |
| 版本管理 | 配置中添加version字段 |
| 回滚机制 | 保留历史配置，支持回滚 |

## 成功案例

### 案例: deepen-langgraph-v2-11-1扩展性设计

**背景**: 需要支持快速接入新Agent/Skill/Memory/项目规则

**应用可插拔扩展架构**:

| 组件 | 发现机制 | 注册机制 | 加载机制 |
|-----|---------|---------|---------|
| Agent | 扫描agents/目录 | AgentRegistry | AgentInvoker动态选择 |
| Skill | 扫描skills/目录 | SkillRegistry | Trigger word匹配 |
| Memory | 扫描memory/目录 | MemoryRegistry | Step匹配自动唤醒 |
| Project Rules | 扫描project-rules/ | RulesRegistry | 合并到Agent输入 |

**成果**:
- 新增Agent: 只需创建agent.md，无需修改代码
- 新增Skill: 只需创建SKILL.md，自动识别trigger_words
- 新增Memory: 只需创建memory.md，自动关联steps
- 项目规则: 只需放到project-rules/，自动加载

---

**模式版本**: v1.0  
**创建日期**: 2026-03-18  
**来源复盘**: deepen-langgraph-v2-11-1技术方案评审过程  
**维护者**: agentsystem架构组
