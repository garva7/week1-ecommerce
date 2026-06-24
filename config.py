import os


class Config:
    # Used to sign the session cookie. Change this to any random string.
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/shopeasy"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
