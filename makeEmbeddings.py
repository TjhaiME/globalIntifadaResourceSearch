from transformers import AutoTokenizer, AutoModel
import torch
from functions import scriptRelativePathToFullPath, get_url_mainText
import os
import json


# Load tokenizer and model from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")



# Function to generate embeddings for combined text
def process_text_embeddings(text):
    
    
    # # Tokenize and create model inputs
    # inputs = tokenizer(text, return_tensors="pt")#FAILS WHEN TEXT IS ABOVE MAX LENGTH
    
    # Tokenize and create model inputs with truncation and max length
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True)
    
    # Generate embeddings
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the embedding for the [CLS] token (or the mean of all tokens)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    
    return embeddings

def make_total_embeddings():
    data = {}
    input_file_path = scriptRelativePathToFullPath('data/data.json')
    print("loading data")
    with open(input_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    totalAmount = len(data)
    counta = 0
    print("about to do embeddings on " + str(totalAmount) + " entries")
    # Loop through your data and update each entry with combined embeddings
    for url, details in data.items():

        counta += 1


        # ##TESTING:
        # if counta > 3:
        #     break

        print("doing embeddings on " + url + "\n      (" + str(counta) + "/" + str(totalAmount) + ")")

        urlMainText = get_url_mainText(url)
        title = details.get("og_title", "")
        summary = details.get("userSummary", "")
        descript = details.get("og_description", "")
        

        combined_text = f"{title} {urlMainText}\n{summary}\n{descript}"

        if combined_text.strip() == "":
            data[url]["cmbEmb_distil"] = []
            continue
    
        combined_embeddings = process_text_embeddings(combined_text)
        
        # Add embeddings to the schema
        data[url]["cmbEmb_distil"] = combined_embeddings.tolist()  # Convert to list for JSON serializability
    print("finished doing embeddings")
    
    finalData = data

    endFilename = scriptRelativePathToFullPath("data/data_with_embeddings.json")
    try:
        with open(endFilename, 'w', encoding='utf-8') as json_file:
            #utf-8 encoding and ensure_ascii=False to save non ascii characters in a normal way for an AI to read later
            #we also need to specify this for beautiful soup in the scrape_og_stuff function
            #json.dump(finalData, json_file, indent=4, ensure_ascii=False)
            json.dump(finalData, json_file, ensure_ascii=False) #TURN INDENT OFF FOR EMBEDDINGS DATA
            #This is okay because we will need to re do the embeddings anyways

        print(f"Data successfully written to {endFilename}")
    except IOError as e:
        print(f"Error writing to file: {e}")




make_total_embeddings()