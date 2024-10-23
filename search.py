import json
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

from functions import scriptRelativePathToFullPath

# Load your JSON dataset
with open(scriptRelativePathToFullPath('data/data_with_embeddings.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

# Function to embed the search query
def embed_text(text):
    # Check if the text is non-empty
    if not text.strip():
        return np.array([])  # Return an empty array if the input is empty
    
    # Tokenize and create model inputs
    inputs = tokenizer(text, return_tensors="pt")
    
    # Generate embeddings
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the embedding (mean of token embeddings)
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    
    return embedding

# Function to compute cosine similarity between two vectors
def compute_cosine_similarity(embedding1, embedding2):
    if embedding1.size == 0 or embedding2.size == 0:
        return 0.0  # Return 0 similarity if one of the embeddings is empty
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# Function to search the dataset
def search(query, data, top_n=5):
    # Embed the search query
    query_embedding = embed_text(query)
    
    if query_embedding.size == 0:
        print("The search query produced an empty embedding.")
        return []
    
    # Create a list to store the similarity scores and results
    results = []

    # Loop through your dataset and calculate similarity
    for urlKey in data.keys():
        # Get the embedding for this entry
        url_embedding = np.array(data[urlKey]["cmbEmb_distil"])
        
        # Skip if the embedding is empty
        if url_embedding.size == 0:
            continue

        # Calculate cosine similarity between the query embedding and the URL embedding
        similarity = compute_cosine_similarity(query_embedding, url_embedding)
        
        # Store the result as a tuple (similarity score, url, userSummary)
        results.append((similarity, urlKey))



    
    # Sort the results by similarity score in descending order
    results = sorted(results, key=lambda x: x[0], reverse=True)
    
    # Return the top N results
    return results[:top_n]

# Example search query
query = "activism tactics"

# Perform the search
top_results = search(query, data, top_n=30)


# Display the search results
for rank, (similarity, url) in enumerate(top_results, 1):
    print(f"Rank {rank}:")
    print(f"URL: {url}")
    print(f"dataset: {data[url]['ogTitle']} \n    {data[url]['userSummary']} \n    {data[url]['ogDescript']}")
    print(f"Category: {data[url]['userTags']}")
    print(f"Similarity Score: {similarity:.4f}")
    print("-" * 50)
