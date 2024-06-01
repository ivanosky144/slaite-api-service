## Getting Started With Slaite.io API Service

## Prerequisities

- Python 3.12
- Docker (if you want to run the app through a container)

## Setup

1. Clone this repo to your local machine:
```
git clone https://github.com/yourusername/slaiteio-api-service.git
```

2. Install dependencies
```
pip install poetry
```
```
poetry install
```

3. Run the app
```
cd app
poetry run uvicorn main:app --reload
```

