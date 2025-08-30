from database import engine, Base
import models  # type: ignore

print("Attempting to create database tables...")

# The Docker healthcheck ensures the DB is ready before this script runs.
# This command creates all tables that inherit from Base in models.py
Base.metadata.create_all(bind=engine)

print("Tables created successfully (if they didn't already exist).")