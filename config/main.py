"""
Holds global config settings for the whole runtime.

Mostly made up of environment config variables.
Also instanciates the `FastAPI()` router instance.
"""
import os
from fastapi import FastAPI

app = FastAPI()

DB_URI = os.environ.get("MONGO_DB_URI")
if not DB_URI:
    raise Exception("Key Error: DB_URI not set!")
