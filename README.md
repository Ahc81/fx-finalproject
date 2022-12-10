# fx-finalproject

## Setup
Create and activate a virtual environment

```sh
conda create -n fx-env python=3.8
```

Activate environment
```sh
conda activate fx-env
```

Install the necessary packages
```sh
pip install -r requirements.txt
```

##Configuration

Obtain an API Key from ALPHAVANTAGE.

Then create a local ".env" file and provide the key like this:
```sh
ALPHAVANTAGE_API_KEY
```

Then create a .gitignore file of the python flavor to help hide the .env file

```sh
.env
```

##Run the code

Follow all of the prompts for the fx_report program
```sh
python -m app.fx_report
```

Follow the prompts and calculate your currency converted
```sh
python -m app.fx_calculate
```

##Run the web_app in local development
```sh
FLASK_APP=web_app flask run
```

