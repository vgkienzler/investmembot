# Investmembot

## How to start?

1. Install the dependencies:
```pip install -r requirements.txt```

2. Copy `.env.sample`, name copy `.env`

3. Add your API keys to the `.env` file

## What to run?

#### Test the script on your local machine:

```python main.py```

#### Test chainlit app on local machine:

```chainlit run app.py```

#### Run Docker container:

```docker build -t investmembot:v0 .```

```docker run investmembot:v0```

## How it works?

1. Upon launch, the app process the docs in the `input/` folder and load their embeddings in the Pinecone vector database,

2. The chainlit app is running on the `localhost:8000` and the user can interact with the app, to ask question pertaining to the documents in the input folder. When an answer cannot be found in the docs, the app look for the answer on the web and returns the answer to the user.

3. Whenever the user ask for the investment memo or a report to be generated, the app will run through the investment memo template and generate a report. The report is saved in the `output/` folder, as a `.docx` file.
