# -*- coding: utf-8 -*-

import os
import nltk

import paddle
import paddle.nn.functional as F
from paddlenlp.data import Tuple, Pad
from paddlenlp.transformers import AutoModelForSequenceClassification, AutoTokenizer


# load the model
if paddle.device.is_compiled_with_cuda():
    paddle.set_device('gpu')
else:
    paddle.set_device('cpu')

base_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_dir, 'pretrained_model')
label_file = os.path.join(base_dir, 'data/label.tsv')
label_list = [ele.strip() for ele in open(label_file).readlines()]
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)
max_seq_length = 512
batch_size = 32

# set nltk data path
nltk_data_path = os.path.join(base_dir, 'nltk_data')
nltk.data.path.append(nltk_data_path)

ATTACK_TACTICS_MAP = {
    'reconnaissance': 'Reconnaissance',
    'resource-development': 'Resource Development',
    'initial-access': 'Initial Access',
    'execution': 'Execution',
    'persistence': 'Persistence',
    'privilege-escalation': 'Privilege Escalation',
    'defense-evasion': 'Defense Evasion',
    'credential-access': 'Credential Access',
    'discovery': 'Discovery',
    'lateral-movement': 'Lateral Movement',
    'collection': 'Collection',
    'command-and-control': 'Command and Control',
    'exfiltration': 'Exfiltration',
    'impact': 'Impact'
}


@paddle.no_grad()
def predict_text(text):
    """
    Predicts the data labels.
    Args:

        text (obj:`str`): text to infer TTPs from.
        
    """

    if not isinstance(text, str):
        return text, None

    if not text:
        return text, [{
            'sent': text,
            'tts': []
        }]

    # splits text to sentences
    sentences = nltk.sent_tokenize(text)
    
    examples = []
    for sent in sentences:
        result = tokenizer(text=sent, max_seq_len=max_seq_length)
        examples.append((result['input_ids'], result['token_type_ids']))

    # separates data into some batches.
    batches = [
        examples[i:i + batch_size]
        for i in range(0, len(examples), batch_size)
    ]

    batchify_fn = lambda samples, fn=Tuple(
        Pad(axis=0, pad_val=tokenizer.pad_token_id),  # input
        Pad(axis=0, pad_val=tokenizer.pad_token_type_id),  # segment
    ): fn(samples)

    preds = []
    model.eval()
    for batch in batches:
        input_ids, token_type_ids = batchify_fn(batch)
        input_ids = paddle.to_tensor(input_ids)
        token_type_ids = paddle.to_tensor(token_type_ids)
        logits = model(input_ids, token_type_ids)
        probs = F.sigmoid(logits).numpy()
        confidence = [] # you can adjust the score value for acceptance, even for each technique prediction
        for prob in probs:
            labels = []
            for i, p in enumerate(prob):
                if p > 0.5:
                    labels.append([i, p])
            preds.append(labels)

    res = []
    for idx, sent in enumerate(sentences):
        labels = []
        for pred, score in preds[idx]:
            tt = label_list[pred]
            ta_n, ta_id, te_name, te_id = tt.split('_')
            ta_n = ATTACK_TACTICS_MAP[ta_n]
            if len(te_id) > 6: # to distinguish sub-techniques
                te_id = te_id[:-3] + "." + te_id[-3:]
            labels.append({
                "tactic_name": ta_n,
                "tactic_id": ta_id,
                "technique_name": te_name,
                "technique_id": te_id,
                "score": score
            })
        res.append({
            "sent": sent,
            "tts": labels
        })

    return text, res