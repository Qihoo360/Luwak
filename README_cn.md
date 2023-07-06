# Luwak TTP Extractor

[English](./README.md) | 简体中文

## 目录
1. [概述](#概述)
2. [背景](#背景)
3. [安装](#安装)
    - [1. 配置虚拟环境](#1-配置虚拟环境)
    - [2. 下载和合并模型](#2-下载和合并模型)
4. [示例](#示例)

## 概述
Luwak TTP Extractor 使用预训练模型从非结构化威胁报告中提取战术、技术和攻击过程 (TTP)。 它使用 [ERNIE](https://github.com/PaddlePaddle/ERNIE) 预训练模型从威胁报告中推断出常见的 TTP。 目前我们只开源了适用英文内容的微调模型。 预计在今年下半年，我们会对外开放一个 TTP 提取服务供试用，该服务支持中文和英文内容。 到时候，我们会把 URL 更新在这里。

## 背景
MITRE ATT&CK 框架使用 TTP 来描述攻击活动中威胁者的的操作模式。TTP 对入侵和攻击模拟（BAS）系统评估防御能力具有价值，同时也是构建基于 TTP 的知识图谱的最重要元素。安全社区中的大多数 TTP 信息存在于非结构化的威胁报告中，例如恶意软件博客、白皮书等。

预训练语言模型在大规模语料上进行预训练，能够学习到通用的语言表示，在诸多下游的自然语言处理任务中成绩优异。从非结构化报告中提取 TTP 本质上是一个文本多分类任务。因此将预训练语言模型来用于下游的 TTP 提取任务，可以达到不错的效果。

## 安装
**关键要求**

- Python (64 bit) >= 3.7
- pip (64 bit) >= 20.2.2
- PaddlePaddle (64 bit) >= 2.0
- paddlenlp
- nltk
- 处理器架构: x86_64 (不支持 arm64 处理器架构)

### 1. 配置虚拟环境
克隆该仓库，通过 virthenv 创建一个虚拟环境并进行配置:
```
pip3 install virtualenv
mkdir <VENV_NAME>
cd <VENV_NAME>
virtualenv -p python3 .
source ./bin/activate
cd <path to this notebook>
pip install -r requirements.txt
```

### 2. 下载和合并模型
下载 nltk punkt 分词模型并合并预训练模型:
```
python -c "import os, nltk; nltk_data_path = os.path.join(os.getcwd(),'nltk_data'); nltk.download('punkt', nltk_data_path);"

./merge_model.sh
```

## 示例
加载模型并导入预测函数：
```
import inference
from inference import predict_text
```

将需要提取 TTP 的文本赋值给变量 `text`:
```
text = """ACNSHELL is sideloaded by a legitimate executable.
It will then create a reverse shell via ncat.exe to the server closed.theworkpc.com"""
```

然后调用函数 `predict_text` 来提取 TTP:
```
o_text, ttps = predict_text(text)
```
变量 `o_text` 存储了输入到函数 `predict_text` 的原始文本。

变量 `ttps` 存储了预测的 TTPs，类似于：
```
[{'sent': 'ACNSHELL is sideloaded by a legitimate executable.',
  'tts': [{'tactic_name': 'Persistence',
    'tactic_id': 'TA0003',
    'technique_name': 'DLLSide-Loading',
    'technique_id': 'T1574.002',
    'score': 0.9799978}]},
 {'sent': 'It will then create a reverse shell via ncat.exe to the server closed.theworkpc.com',
  'tts': [{'tactic_name': 'Execution',
    'tactic_id': 'TA0002',
    'technique_name': 'WindowsCommandShell',
    'technique_id': 'T1059.003',
    'score': 0.98543674}]}]
```
每个句子（由 `sent` 域指定）可能映射零个或多个技战术（由 `tts` 域指定）。对于每个预测的技战术，`tactic_name` 和 `tactic_id` 域分别指定战术的名称和 ID，`technique_name` 和 `technique_id` 分别指定技术的名称和 ID，`score` 域给出了模型对该技战术的预测分数。
