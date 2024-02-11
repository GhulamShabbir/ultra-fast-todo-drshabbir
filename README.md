# Ultra Fast Todo App

## Setup and Run the App

### Create venv

#### Using CMD

```shell
python -m venv venv 
venv\Scripts\activate
```

OR

#### Using Powershell

```shell
python -m venv venv 
.\venv\Scripts\Activate.ps1
```

OR

#### Using bash

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install requirements

```shell
python -m pip install -r requirements.txt
```

### Run app

```shell
uvicorn main:app --reload
```

### Run test cases

```shell
python -m pytest
```
