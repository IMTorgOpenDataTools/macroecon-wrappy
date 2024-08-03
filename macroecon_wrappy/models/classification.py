#!/usr/bin/env python3
"""
Module Docstring

"""
'''
#TODO:from nltk.tokenize import word_tokenize 

import torch
#from transformers import AutoModel
from setfit import SetFitModel
'''
from pathlib import Path
import re

'''
#load models
#config_env.config()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = Path("pretrained_models/finetuned--BAAI")
model = SetFitModel.from_pretrained(model_path)
model.to(device)
'''

def classifier(chunk):
    """Importable function to run assigned models."""
    result = []
    models = [
        kw_classifier,
        #phrase_classifier,
        #fs_classifier
    ]
    for model in models:
        result.append( model(chunk) )

    return result


def kw_classifier(chunk):
    """..."""

    data_path = Path('./macroecon_wrappy/models/data')
    with open(data_path / 'pos_kw.txt', 'r') as file:
        kw_lines = file.readlines()
    KEYWORDS = [f"{word.replace('\n','')}" for word in kw_lines]      #consider spacing around word

    result = {
        'search': 'KW',
        'target': None,
        'timestamp': None,
        'pred': None
        }
    hits = []
    for word in KEYWORDS:
        starts = [m.start() for m in re.finditer(word, chunk)]
        hits.extend(starts)
    #FIX THE REST OF THIS LOGIC BASED ON NEEDS
    if len(hits)>0:
            result['target'] = KEYWORDS
            result['index'] = hits
            result['pred'] = len(hits) / len(chunk)
            return result
    else:
        return None
    
'''
def phrase_classifier(chunk):
    """..."""
    return None


def fs_classifier(chunk):
    """..."""
    result = {
        'search': 'FS',
        'target': None,
        'timestamp': None,
        'pred': None
        }
    if len(chunk['text']) > 40:
        probs = model.predict_proba(chunk['text'])
        pos_idx = model.labels.index('positive')
        prob_positive = probs.tolist()[pos_idx]
        if prob_positive > .5:
            result['target'] = chunk['text']
            result['timestamp'] = chunk['timestamp']
            result['pred'] = prob_positive
            return result
    return None
'''