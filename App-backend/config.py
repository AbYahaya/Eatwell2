import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'Eatwell')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///restaurants.db')  # Update this to your production database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'EatwellJWT')