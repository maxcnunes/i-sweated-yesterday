from app import db

# Drop all tables from db file
db.drop_all() 

# Create all tables on db file,
# copying the structure from the definition on the Models
db.create_all()