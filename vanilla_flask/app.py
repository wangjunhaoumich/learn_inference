#%%
import io
import json

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import torch._dynamo as torchdynamo
import torch
from flask import Flask, jsonify, request


app = Flask(__name__)
torchdynamo.config.cache_size_limit = 512

model_name = "t5-base"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.generate2 = torchdynamo.optimize("inductor")(model.generate)
model = model.eval().cuda()

tokenizer = AutoTokenizer.from_pretrained(model_name)
model.eval()

#%%
def transform_text(text):
    tensors = tokenizer(text, return_tensors='pt', padding='max_length', 
        max_length=20, truncation=True).to('cuda')
    print(tensors['input_ids'].shape)
    return tensors


def get_prediction(text):
    tensor = transform_text(text)
    with torch.inference_mode():
        outputs = model.generate2(max_length=20, **tensor)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return decoded


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.json['text']
        out_text = get_prediction(text)
        return jsonify({'out_text': out_text})

#%%
if __name__ == '__main__':
    app.run()