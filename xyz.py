from sqlalchemy import create_engine, text

# Replace 'sqlite:///your_database.db' with the URL of your SQLite database
engine = create_engine('sqlite:///site.db')

# Establish a connection
with engine.connect() as connection:
    # Use a text SQL statement to delete records from alembic_version
    delete_statement = text("DELETE FROM alembic_version")
    
    # Execute the delete statement
    connection.execute(delete_statement)
