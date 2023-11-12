# Nuforc-Webscraper
A Web Scraper for the Nuforc website, build with Scrapy.

### Installation
> Before installing and running this repo locally, you need to have [Docker](https://docs.docker.com/engine/install/) and [MongoDB](https://www.mongodb.com/docs/manual/installation/) set up on your computer, with a MongoDB instance running. 

Install Via GitHub CLI:
```
gh repo clone AIEdit/Nuforc-Webscraper
```

while optional, it is highly reccomended to create a virtual env for this project.
```
python3.11 -m venv venv
source ./bin/scripts/activate
```

Once complete, nessecary packages may be installed via the requirements.txt file
```
pip install -r requirements.txt
```

## TODO
 - Support for alternatives to MongoDB, namely the following: 
    - Postgresql
    - JSONL
- Improved implementation utilizing Nuforc's APIs