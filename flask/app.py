from flask import Flask, request, render_template
import json
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

from functions import scriptRelativePathToFullPath

# Define the app
app = Flask(__name__)

# Load your JSON dataset (adjust the path as necessary)
with open(scriptRelativePathToFullPath('data/data_with_embeddings.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

# Function to embed the search query
def embed_text(text):
    if not text.strip():
        return np.array([])  # Return an empty array if the input is empty
    
    inputs = tokenizer(text, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    
    return embedding

# Function to compute cosine similarity between two vectors
def compute_cosine_similarity(embedding1, embedding2):
    if embedding1.size == 0 or embedding2.size == 0:
        return 0.0  # Return 0 similarity if one of the embeddings is empty
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# Function to search the dataset
def search(query, data, top_n=5):
    query_embedding = embed_text(query)
    
    if query_embedding.size == 0:
        return []

    results = []

    for urlKey in data.keys():
        url_embedding = np.array(data[urlKey]["cmbEmb_distil"])
        
        if url_embedding.size == 0:
            continue

        similarity = compute_cosine_similarity(query_embedding, url_embedding)
        results.append((similarity, urlKey))
    
    results = sorted(results, key=lambda x: x[0], reverse=True)
    
    return results[:top_n]

# Route for the search page
@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""

    if request.method == 'POST':
        query = request.form['query']  # Get the search query from the form
        results = search(query, data, top_n=10)

    return render_template('index.html', query=query, results=results, data=data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
