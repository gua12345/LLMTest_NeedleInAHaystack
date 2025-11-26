# OpenAI兼容接口测试函数使用说明

## 概述

这个测试函数用于测试OpenAI兼容接口的模型在"大海捞针"任务中的表现。测试会在不同长度和深度的上下文中插入多个"针"（特定信息），然后测试模型能否准确检索出这些信息。

## 文件位置

测试函数位于：`needlehaystack/test_openai_compatible.py`

## 使用方法

### 1. 环境准备

确保已安装项目依赖：
```bash
pip install -r requirements.txt
```

### 2. 设置API密钥

设置环境变量：
```bash
# Windows PowerShell
$env:NIAH_MODEL_API_KEY = "your-api-key-here"
$env:NIAH_EVALUATOR_API_KEY = "your-evaluator-api-key-here"

# 或者
set NIAH_MODEL_API_KEY=your-api-key-here
set NIAH_EVALUATOR_API_KEY=your-evaluator-api-key-here
```

### 3. 修改测试配置

打开 `test_openai_compatible.py` 文件，在以下位置修改你的配置：

```python
# ===== 在这里修改你的模型配置 =====
# 修改为你要测试的OpenAI兼容模型名称
MODEL_NAME = "gpt-3.5-turbo-0125"  # 可以改为其他模型如 "gpt-4" 等

# 修改为你的OpenAI兼容API端点（如果不是使用OpenAI官方API）
# 如果使用OpenAI官方API，可以保持None
OPENAI_BASE_URL = None  # 例如: "https://api.your-provider.com/v1"

# 修改为你的API密钥环境变量名
API_KEY_ENV = "NIAH_MODEL_API_KEY"
# ====================================
```

### 4. 运行测试

```bash
cd needlehaystack
python test_openai_compatible.py
```

## 测试参数说明

- **needles**: 插入到上下文中的多个"针"信息
- **context_lengths_min/max**: 测试的上下文长度范围
- **context_lengths_num_intervals**: 上下文长度的测试间隔数
- **document_depth_percent_min/max**: "针"插入深度的百分比范围
- **document_depth_percent_intervals**: 深度测试的间隔数

## 大上下文模型测试建议

对于大上下文模型（如64k-128k），建议使用以下参数设置：

```python
context_lengths_min=64000,        # 最小上下文长度
context_lengths_max=128000,       # 最大上下文长度
context_lengths_num_intervals=5,   # 测试间隔数
```

这样可以测试模型在不同上下文长度下的表现：
- 64k tokens
- 80k tokens
- 96k tokens
- 112k tokens
- 128k tokens

如果需要更精细的测试，可以增加 `context_lengths_num_intervals` 的值。

## 测试结果

测试完成后，会显示：
- 总测试数
- 平均分数
- 最高分数
- 最低分数

详细结果会保存到JSON文件中，文件名格式为：
`test_results_{模型名}_{时间戳}.json`

## 自定义测试

如需自定义测试参数，可以修改 `LLMMultiNeedleHaystackTester` 的初始化参数：

```python
tester = LLMMultiNeedleHaystackTester(
    needles=needles,  # 自定义"针"信息
    model_to_test=model_provider,
    evaluator=evaluator,
    retrieval_question="你的问题",  # 自定义检索问题
    context_lengths_min=1000,  # 最小上下文长度
    context_lengths_max=16000,  # 最大上下文长度
    # ... 其他参数
)
```

## 注意事项

1. 确保API密钥有足够的配额
2. 测试可能需要较长时间，取决于测试参数设置
3. 测试结果会保存在 `results` 和 `contexts` 目录中
4. 如果使用非OpenAI官方API，请确保API兼容OpenAI格式