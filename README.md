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
