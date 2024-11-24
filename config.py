import os

class Config:
    SECRET_KEY = "super_secret_key"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:i8xr-3qtr-ylt7@localhost/task_checker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "uploads/"

