To create a venv for fast api

cmd : python -m venv my_env


To activate the venv

cmd : my_venv/Scripts/activate 


To install the fastapi

cmd : pip install fastapi[all]


To install the uvicorn

cmd : pip install uvicorn[standard]


To run the server

cmd : uvicorn main:app --reload