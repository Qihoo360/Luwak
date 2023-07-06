# Luwak TTP Extractor

English | [简体中文](./README_cn.md)

## Table of Content
1. [Overview](#overview)
2. [Background](#background)
3. [Setup](#setup)
    - [1. Setup Virtual Env](#1-setup-virtual-env)
    - [2. Download and Merge Model Artifacts](#2-download-and-merge-model-artifacts)
4. [Demo](#demo)

## Overview
Luwak TTP Extractor uses pre-trained models to extract Tactics, Techniques and Procedures (TTPs) from unstructured threat reports. It uses [ERNIE](https://github.com/PaddlePaddle/ERNIE) pre-trained models to infer common TTPs from threat reports. Currently, we only open source the fine-tuned model for English content. It is expected that in H2, we will have an external TTP extraction service for trial use. It supports Chinese and English content. When the time comes, we will update the URL here.

## Background
MITRE ATT&CK is a framework which uses TTPs to describe the operation modes in campaigns of threat actors. TTPs are valuable to Breach and Attack Simulation (BAS) system to assess defense capabilities, and are the most important parts of TTP-based Knowledge Graph. Most TTPs of threat actors in security community exist in unstructured threat reports, such as malware blogs and white papers.

The pre-trained language model is pre-trained on a large-scale corpus, thus it can learn a general language representation, and has excellent results in many downstream natural language processing tasks. Extracting TTPs from unstructured reports is essentially a text multi-classification task. Therefore, using the pre-trained language model for downstream TTP extraction task can achieve good results.

## Setup
**Key Requirements**

- Python (64 bit) >= 3.7
- pip (64 bit) >= 20.2.2
- PaddlePaddle (64 bit) >= 2.0
- paddlenlp
- nltk
- Processor arch: x86_64 (arm64 is not supported)

### 1. Setup Virtual Env
Clone the repository and setup a virtual env with virthenv:
```
pip3 install virtualenv
mkdir <VENV_NAME>
cd <VENV_NAME>
virtualenv -p python3 .
source ./bin/activate
cd <path to this notebook>
pip install -r requirements.txt
```

### 2. Download and Merge Model Artifacts
Download nltk punkt and merge pretrained model:
```
python -c "import os, nltk; nltk_data_path = os.path.join(os.getcwd(),'nltk_data'); nltk.download('punkt', nltk_data_path);"

./merge_model.sh
```

## Demo
Load the model and import predict function:
```
import inference
from inference import predict_text
```

Put the text to extract TTPs in the `text` variable:
```
text = """ACNSHELL is sideloaded by a legitimate executable.
It will then create a reverse shell via ncat.exe to the server closed.theworkpc.com"""
```

Then call the `predict_text` function to infer TTPs:
```
o_text, ttps = predict_text(text)
```
The `o_text` variable stores the original text which is the input of `predict_text` function.

The `ttps` variable stores the predicted TTPs, it looks like:
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
Every sentence (specified by the `sent`) may maps zero or serveral tactics and techniques (specified by `tts`). For each predicted tactic and technique, the fields `tactic_name` and `tactic_id` indicate the name and id of tactic, the fields `technique_name` and `technique_id` indicate the name and id of technique, the field `score` gives the model's score for the tactic and technique.
