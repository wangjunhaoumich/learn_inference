#%%
import requests
import json 
# %%
import time
start = time.time()
for _ in range(10):
    resp = requests.post("http://localhost:5000/predict", json={'text': 'hello ' * 20})
    print(resp.json())
end = time.time()
print((end - start) / 10)
# %%
