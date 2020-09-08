
import re
import pickle
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
import requests
from flask import jsonify

payload = {'i' : 1000, 'sort' : 'desc'}
result = requests.get("http://0.0.0.0:3000/get_data", payload, headers={"Content-Type":"application/json"})
result.json()
result = result.json()
arry1 = []
arry2 = []
for i, k in result['data']:
    arry1.append(i)
    arry2.append(k)

def clean_text(text):
    text = text.lower()
    text = re.sub("@[a-z0-9_]+", ' ', text)
    text = re.sub("[^ ]+\.[^ ]+", ' ', text)
    text = re.sub("[^ ]+@[^ ]+\.[^ ]", ' ', text)
    text = re.sub("[^a-z\' ]", ' ', text)
    text = re.sub(' +', ' ', text)

    return text

cleaned_test = []
for i in arry1:
    cleaned = clean_text(i)
    cleaned_test.append(cleaned)

with open('ilk_projem/model.pickle', 'rb') as file:
    model = pickle.load(file)
with open('ilk_projem/vectorizer.pickle', 'rb') as file:
    vectorizer = pickle.load(file)

payload = {'label' : 'all text', 'count' : 1000}
resu = requests.get("http://0.0.0.0:3000/get_data_count", payload, headers={"Content-Type":"application/json"})
res = resu.json()
print(res)

example_test = vectorizer.transform(cleaned_test)
example_result = model.predict(example_test)
print(example_result)
print(accuracy_score(arry2, example_result))
