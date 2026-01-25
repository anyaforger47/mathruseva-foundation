import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mathruseva_foundation_2024_secure_key')
    
    # Database configuration for production
    MYSQL_CONFIG = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'user': os.environ.get('DB_USER', 'root'),
        'password': os.environ.get('DB_PASSWORD', 'NehaJ@447747'),
        'database': os.environ.get('DB_NAME', 'mathruseva_foundation')
    }
