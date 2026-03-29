import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_LINK")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# DB_LINK = "postgresql://{user}:{password}@{host}:5432/{database_name}"
