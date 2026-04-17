"""
Claude 课程 — 第六章演示脚本
AI 编程助手（对应 Claude Code 与 Computer Use 概念）
===================================
说明：Claude Code 是 CLI 工具，本脚本演示 AI 编程助手的核心能力：
      代码理解、生成、重构、调试、测试生成
使用方法：python 06_AI编程助手演示.py
依赖安装：pip install openai python-dotenv
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("LKEAP_API_KEY", "your-api-key-here"),
    base_url="https://tokenhub.tencentmaas.com/v1",
)
MODEL = "glm-5"
THINKING_OFF = {"thinking": {"type": "disabled"}}

CODE_SYSTEM = "你是一位资深软件工程师，擅长代码分析、重构和调试。回答要简洁专业，直接给出代码和说明。"


def call(user_msg, system=CODE_SYSTEM, max_tokens=3000, extra=None):
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user_msg})
    kwargs = dict(model=MODEL, messages=msgs, max_tokens=max_tokens)
    if extra:
        kwargs["extra_body"] = extra
    return client.chat.completions.create(**kwargs).choices[0].message.content


# ─────────────────────────────────────────────
# 演示 1：代码理解 —— 解释代码逻辑
# ─────────────────────────────────────────────
def demo_code_explain():
    print("=" * 55)
    print("演示 1：代码理解 —— 解释代码逻辑")
    print("=" * 55)

    code = '''
def lru_cache(capacity):
    cache = {}
    order = []
    def get(key):
        if key not in cache:
            return -1
        order.remove(key)
        order.append(key)
        return cache[key]
    def put(key, value):
        if key in cache:
            order.remove(key)
        elif len(cache) >= capacity:
            oldest = order.pop(0)
            del cache[oldest]
        cache[key] = value
        order.append(key)
    return get, put
'''

    prompt = f"请解释这段代码的作用、核心逻辑，并指出其潜在的性能问题：\n```python{code}```"
    result = call(prompt)
    print(result)
    print()


# ─────────────────────────────────────────────
# 演示 2：代码生成 —— 根据需求生成代码
# ─────────────────────────────────────────────
def demo_code_generation():
    print("=" * 55)
    print("演示 2：代码生成 —— 根据需求生成实现")
    print("=" * 55)

    requirement = """
请用 Python 编写一个函数 `retry_with_backoff`，实现：
1. 对任意函数进行重试，最多重试 3 次
2. 每次重试间隔指数增长：1s → 2s → 4s
3. 支持指定可重试的异常类型
4. 重试失败后抛出最后一次异常
5. 加上完整的类型注解和 docstring
"""
    result = call(requirement)
    print(result)
    print()


# ─────────────────────────────────────────────
# 演示 3：代码重构 —— 优化已有代码
# ─────────────────────────────────────────────
def demo_code_refactor():
    print("=" * 55)
    print("演示 3：代码重构 —— 优化代码质量")
    print("=" * 55)

    bad_code = '''
def p(l):
    r = []
    for i in range(len(l)):
        if l[i] % 2 == 0:
            r.append(l[i] * l[i])
    return r

def main():
    data = [1,2,3,4,5,6,7,8,9,10]
    result = p(data)
    for i in range(len(result)):
        print(result[i])
'''

    prompt = f"""请重构以下代码，要求：
1. 使用 Pythonic 风格（列表推导式、生成器等）
2. 改善命名（函数名、变量名要有意义）
3. 添加类型注解
4. 给出重构前后对比说明

```python{bad_code}```"""

    result = call(prompt)
    print(result)
    print()


# ─────────────────────────────────────────────
# 演示 4：Bug 定位与修复
# ─────────────────────────────────────────────
def demo_debug():
    print("=" * 55)
    print("演示 4：Bug 定位与修复")
    print("=" * 55)

    buggy_code = '''
def find_duplicates(nums: list) -> list:
    """找出列表中的重复元素"""
    seen = set()
    duplicates = set()
    for num in nums:
        if num in seen:
            duplicates.add(num)
        seen.add(num)
    return list(duplicates)

# 测试
print(find_duplicates([1, 2, 3, 2, 4, 3, 5]))  # 期望: [2, 3]
print(find_duplicates([1, 1, 1, 1]))              # 期望: [1]，实际正确
print(find_duplicates([]))                         # 期望: []，实际正确

# 但这个场景有问题：
result = find_duplicates([1, 2, 3, 4, 5])
print(f"排序后的重复：{sorted(result)}")  # 期望有序输出，但 set 无序
'''

    prompt = f"""分析以下代码，找出所有潜在问题（不只是明显的 bug），并给出修复版本：

```python{buggy_code}```

请按照：问题分析 → 修复代码 → 测试验证 的结构回答。"""

    result = call(prompt)
    print(result)
    print()


# ─────────────────────────────────────────────
# 演示 5：自动生成单元测试
# ─────────────────────────────────────────────
def demo_test_generation():
    print("=" * 55)
    print("演示 5：自动生成单元测试")
    print("=" * 55)

    target_code = '''
def parse_config(config_str: str) -> dict:
    """
    解析简单的 key=value 格式配置字符串
    支持注释（#开头的行）和空行
    返回配置字典，值统一为字符串类型
    """
    result = {}
    for line in config_str.strip().split("\\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f"Invalid config line: {line}")
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result
'''

    prompt = f"""为以下函数生成完整的 pytest 单元测试，要求覆盖：
1. 正常情况（含注释、空行）
2. 边界情况（空字符串、只有注释）
3. 异常情况（非法格式）
4. 值中包含等号的情况（如 url=http://example.com）

```python{target_code}```"""

    result = call(prompt)
    print(result)
    print()


# ─────────────────────────────────────────────
# 演示 6：Computer Use 概念说明（文字演示）
# ─────────────────────────────────────────────
def demo_computer_use_concept():
    print("=" * 55)
    print("演示 6：Computer Use 概念理解")
    print("=" * 55)

    prompt = """请解释 Computer Use（AI桌面操控）的核心工作原理，需要说明：
1. 截图→坐标→动作的基本循环是什么
2. 它与普通 API 调用的本质区别
3. 实际使用场景举例（3个）
4. 当前主要限制和注意事项

回答要简洁，用工程师能快速理解的语言。"""

    result = call(prompt, extra=THINKING_OFF)
    print(result)
    print()


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Claude 课程第六章 — AI 编程助手（Claude Code 核心能力）")
    print(f"   模型：{MODEL}\n")

    demo_code_explain()
    demo_code_generation()
    demo_code_refactor()
    demo_debug()
    demo_test_generation()
    demo_computer_use_concept()

    print("✅ 第六章演示完成！")
