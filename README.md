# Global Intifada Resource Search

This project processes and organizes a dataset of useful resources for the Tech4Palestine initiative. It categorizes and embeds the data for easy search functionality, with both command-line and web-based search options.
A lot of code was generated with the assistance of chatGPT, but if it works it works. If you don't like it please make it better.

optional: open a virtual environment

pip install -r requirements.txt
to install all dependencies

python flask/app.py to open the search application on your local browser



## Dataset Overview

The dataset was initially obtained manually from the Tech4Palestine Discord server under the "useful resources" section. The raw, unorganized data can be found inside the `uncleanedData` folder.

## Data Processing Steps

1. **Categorization and Dictionary Creation**
   - The uncleaned data was categorized and passed into ChatGPT to transform it into a Python dictionary format.
   - The URLs are used as keys, and the values are dictionaries containing:
     - `userSummary`: A brief description of the resource.
     - `category`: A tag categorizing the resource.
   - This data was stored in `summary.py`.

2. **Converting to JSON**
   - At the bottom of `summary.py`, there is code to convert the dictionary into a JSON format.
   - The `getURLSnippet.py` script is used to scrape the `og_description` and `og_title` from each URL or log any errors encountered during scraping.

3. **Handling Additional Links**
   - The `moreToAdd.py` file contains links that require further work before they can be processed.

4. **Embedding with DistilBERT**
   - The `makeEmbeddings.py` script is used to generate vector embeddings for the combined text using the DistilBERT model.
   - The embeddings are saved into a separate JSON file for further use.

## Search Functionality

- **Static Search (Command Line)**
  - The `search.py` script can be used to perform searches by specifying a static search prompt in the code.

- **Flask Application (Web Interface)**
  - The project includes a Flask-based web application that allows users to search the resources using natural language processing.
  - To run the Flask application locally:
    
    python flask/app.py
    
  - This launches a local server running on `localhost`, allowing for easy, interactive searches. The AI is hosted locally, but the system can be easily adapted for use on a website.

## To-Do

- The `moreToAdd.py` file contains links that need additional processing before they can be fully integrated into the dataset.
- Fix various problems mentioned in problems.txt
- 

---

Feel free to reach out for any issues or contributions to the project!
