# An Agenda Example

## Description
This project is an example of FastAPI usage for a simple project.
The intention here is provide a simple API for getting contact information


## Denpendencies
The project runs on python 3.12.x. We suggest using virtual So you have to
install virtualenv(20.23.x recommended) and virtualenvwrapper for convenience.

## How to install dependencies
1. Create a virtualenv. Example: agendaBackend
   1.  (https://itslinuxfoss.com/install-virtualenv-ubuntu-22-04/)
   2.  https://virtualenvwrapper.readthedocs.io/en/latest/install.html
2. Inside virtualenv update pip to latest version: $pip install -U pip
3. Install project dependencies. pip install -r requirements.txt


## How to run the server
Moving to "src" folder execute:
 $ uvicorn --host 0.0.0.0 --port 8000 --reload main:app


## How to stop the server
Just press CTRL + C in terminal where server is executing
