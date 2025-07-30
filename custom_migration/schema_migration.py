from sqlalchemy import text
from sqlalchemy.orm import Session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.db import engine


custom_command = "SELECT * FROM account LIMIT 1"


with engine.connect() as connection:
    result = connection.execute(text("""
        SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast', 'pg_temp_1', 'pg_toast_temp_1')
      AND schema_name NOT LIKE 'pg_%'
      AND schema_name LIKE 'tenant_%'
    """
))
schemas = [row[0] for row in result]

print(schemas)

for schema in schemas:
        print(f"-------------Execut în schema: {schema} -------------\n")
        try:
            with Session(engine) as session:
                session.execute(text(f'SET search_path TO "{schema}"'))
                session.execute(text(custom_command))
                session.commit()
        except Exception as e:
            print(f"Eroare în schema {schema}: {e}")