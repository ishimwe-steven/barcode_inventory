import os

class Config:
    SECRET_KEY = 'supersecretkey'  # Change to a secure key in production
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_QtuPajcS6YI4@ep-wispy-darkness-aei79rpl-pooler.c-2.us-east-2.aws.neon.tech/barcode_inventory?sslmode=require&channel_binding=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
