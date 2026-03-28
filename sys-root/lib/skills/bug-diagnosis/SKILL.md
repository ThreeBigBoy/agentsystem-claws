# Bug 诊断与修复 Skill

## 触发场景

当遇到以下情况时，必须立即调用本 Skill：
- 代码执行结果与预期不符
- 测试失败、运行时错误、异常
- 多次修复仍无法根除问题
- 出现"修了一个问题又出另一个问题"的感觉
- 递归调用、无限循环问题
- 输出格式不符合预期

## 核心认知

### 最重要的是"停下来"

```
行动者模式（看到问题就立刻修）：
问题A → 修复A → 问题B → 修复B → 问题C → 修复C → ...

观察者模式（先停下来观察）：
问题C → 停下来 → 发现A、B、C有关联 → 分析 → 找到根因 → 根本解决
```

**"停下来"比"解决问题"更重要！**

---

## 核心能力模型

### 1. 问题定位（Problem Localization）

#### 1.1 调用链路追踪
```
执行流程：
1. 确定问题入口点（函数/API/命令行）
2. 追踪每层调用，检查参数传递
3. 识别边界：同步/异步、子进程、父进程
4. 验证每层是否正确执行
```

**常用命令**：
```bash
# 追踪Python调用
python -c "import traceback; traceback.print_stack()"

# 追踪subprocess调用
strace -f python script.py  # Linux
# 或
python -v script.py 2>&1 | grep -E "(import|call)"
```

#### 1.2 日志与输出分析
```
分析方法：
1. 区分 stdout vs stderr
2. 提取关键信息：错误类型、消息、堆栈
3. 时间戳对齐（如果有多进程/多线程）
4. 模式匹配：重复出现、异常值
```

#### 1.3 边界条件识别
```
常见边界：
- 空值 vs None
- 0 vs 空字符串 vs 空列表
- 超时边界（30s vs 60s）
- 递归深度限制
- 文件路径存在性
- 权限问题
```

### 2. 根因分析（Root Cause Analysis）

#### 2.1 5 Why 分析法
```
问题发生时，连续追问5个为什么：

Why 1: [观察现象]
  → [直接原因]

Why 2: [为什么会这样]
  → [中层原因]

Why 3: [为什么中层会这样]
  → [深层原因]

Why 4: [为什么深层是这个]
  → [系统原因]

Why 5: [为什么系统这样设计]
  → [根本原因]
```

#### 2.2 层次溯源法
```
问题可能出现在哪一层？
- 表现层：输入/输出格式、UI显示
- 业务逻辑层：算法、流程、条件判断
- 接口层：API契约、参数校验
- 基础设施层：文件、网络、进程
- 架构层：设计缺陷、模块边界
```

#### 2.3 假设验证法
```
步骤：
1. 根据现象提出可能假设
2. 设计最小实验验证假设
3. 排除或确认每个假设
4. 找到最小可复现路径

示例：
假设A：timeout=30导致超时
验证：改为timeout=60，观察是否解决
```

### 3. 修复策略（Fix Strategy）

#### 3.1 最小改动原则
```
目标：在解决问题的同时，减少副作用

检查清单：
□ 是否只改了必要的代码？
□ 是否避免了"过度修复"？
□ 是否有更简单的实现方式？
□ 改动是否向后兼容？
```

#### 3.2 回归测试策略
```
测试层次：
1. 单元测试：改动的函数是否正常？
2. 集成测试：相关模块是否正常？
3. 端到端测试：整体流程是否正常？
```

#### 3.3 修复验证清单
```
□ 修复后问题不再复现
□ 相关功能未被破坏
□ 性能未明显下降
□ 代码风格一致
```

### 4. 模式识别（Pattern Recognition）

#### 4.1 常见 Bug 模式

| 模式 | 特征 | 排查方法 |
|------|------|---------|
| **递归陷阱** | 调用栈溢出、无限循环 | 检查是否有终止条件 |
| **竞态条件** | 偶发性失败、时序相关 | 添加日志、重复执行 |
| **资源泄漏** | 内存增长、文件句柄耗尽 | 监控资源使用 |
| **超时问题** | 请求挂起、进程卡死 | 检查timeout设置 |
| **输出格式问题** | JSON解析失败、格式混乱 | 验证输出隔离 |
| **参数传递问题** | 上一层的值没有传递到下一层 | 追踪调用链 |

#### 4.2 架构问题模式

| 模式 | 特征 | 解决方案 |
|------|------|---------|
| **循环依赖** | A→B→A | 引入中间层/接口 |
| **层次越界** | 上层调用不应该调用的下层 | 明确层次边界 |
| **职责不清** | 模块承担多个无关职责 | 拆分模块 |

### 5. 调试工具箱

#### 5.1 Python 调试
```python
# 打印变量值
print(f"DEBUG: var={var}")

# 打印调用栈
import traceback
traceback.print_stack()

# 计时装饰器
from functools import wraps
import time
def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        print(f"{f.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper
```

#### 5.2 Subprocess 调试
```python
# 分离 stdout 和 stderr
proc = subprocess.run(cmd, capture_output=True, text=True)
print(f"stdout: {proc.stdout}")
print(f"stderr: {proc.stderr}")
print(f"returncode: {proc.returncode}")

# 超时处理
try:
    proc = subprocess.run(cmd, timeout=60)
except subprocess.TimeoutExpired:
    print("命令超时！")
```

#### 5.3 JSON 解析调试
```python
import json

def extract_json_safe(stdout):
    """安全提取JSON"""
    lines = stdout.strip().split('\n')
    for i, line in enumerate(lines):
        if line.strip().startswith('{'):
            try:
                return json.loads('\n'.join(lines[i:]))
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}")
    return None
```

## 执行流程

```
当遇到bug时：

1. 【问题定位】
   ├─ 识别问题入口
   ├─ 追踪调用链路
   └─ 提取关键日志/输出

2. 【根因分析】
   ├─ 5 Why 追问
   ├─ 层次溯源
   └─ 假设验证

3. 【模式匹配】
   ├─ 匹配常见模式？
   └─ 制定修复策略

4. 【实施修复】
   ├─ 最小改动
   ├─ 添加测试
   └─ 验证修复

5. 【沉淀经验】
   ├─ 记录问题现象
   ├─ 记录根因
   ├─ 记录修复方案
   └─ 提取模式到 memory
```

## 输出格式

修复完成后，必须输出：

```markdown
## Bug 修复报告

### 问题现象
[描述观察到的异常]

### 根因分析
[5 Why 分析结果]
[层次溯源结论]

### 修复方案
[具体改动]
[最小改动检查]

### 验证结果
[测试结果]
[相关功能是否正常]

### 经验沉淀
[提取的模式]
[建议添加到 memory 的内容]
```

## 相关 Memory

- `anti-pattern-conditional-pass-as-go.md` - 条件通过陷阱
- `anti-pattern-runtime-logs-business-data-pitfall.md` - 运行时日志陷阱
- `reflection-bug-fix-two-layer-recursion-problem.md` - 两层递归问题案例
