import os
from urllib import request

def read_folder_contents(folder_path):
    try:
        # List all files and subdirectories in the given folder
        contents = os.listdir(folder_path)

        # Print the contents of the folder
        print(f"Contents of folder {folder_path}:")
        for item in contents:
            print(item)

    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
folder_path =  r'C:\Users\jerold\Downloads\ora2pg_dump'
read_folder_contents(folder_path)


import os
import re

def extract_unique_name(folder_name):
    # Use regular expression to extract the unique part of the folder name
    match = re.match(r'ORA2PG_DUMP_(\d+)', folder_name)
    if match:
        return match.group(1)
    else:
        return None

def get_unique_folder_names(base_folder_path):
    # List all folders in the base directory
    folders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]

    unique_names = set()

    for folder in folders:
        unique_name = extract_unique_name(folder)
        if unique_name:
            unique_names.add(unique_name)

    return list(unique_names)

# Example usage:
base_folder_path = r'C:\Users\jerold\Downloads\ora2pg_dump'
unique_folder_names = get_unique_folder_names(base_folder_path)

print("Unique folder names:")
for name in unique_folder_names:
    print(name)



import os
import re

def extract_unique_name(folder_name):
    # Use regular expression to extract the unique part of the folder name
    match = re.match(r'ORA2PG_DUMP_(\d+)', folder_name)
    if match:
        return match.group(1)
    else:
        return None

def get_unique_folder_names(base_folder_path):
    # List all folders in the base directory
    folders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]

    unique_names = set()

    for folder in folders:
        unique_name = extract_unique_name(folder)
        if unique_name:
            unique_names.add(unique_name)

    return list(unique_names)

def read_sql_files(folder_path, folder_name):
    sql_files = [f for f in os.listdir(folder_path) if f.endswith('.sql') and f.startswith('ora2pg_dump')]
    
    if sql_files:
        print(f"Files in folder '{folder_name}':")
        for sql_file in sql_files:
            print(f"- {sql_file}")
        print()

# Example usage:
base_folder_path = r'C:\Users\jerold\Downloads\ora2pg_dump'
unique_folder_names = get_unique_folder_names(base_folder_path)

for unique_name in unique_folder_names:
    folder_name = f'ORA2PG_DUMP_{unique_name}'
    folder_path = os.path.join(base_folder_path, folder_name)
    read_sql_files(folder_path, folder_name)



import os
import re
import psycopg2
def create_database_ora2():
    try:
        connection = db_connection
        database_name = request.form['database_name']
        create_db_postgres(connection, database_name)
        connection.close()
        return f"Database '{database_name}' created successfully."
    except Exception as e:
        return f"Error: {str(e)}"
    
def extract_unique_name(folder_name):
    # Use regular expression to extract the unique part of the folder name
    match = re.match(r'ORA2PG_DUMP_(\d+)', folder_name)
    if match:
        return match.group(1)
    else:
        return None

def get_unique_folder_names(base_folder_path):
    # List all folders in the base directory
    folders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]

    unique_names = set()

    for folder in folders:
        unique_name = extract_unique_name(folder)
        if unique_name:
            unique_names.add(unique_name)

    return list(unique_names)

def schema_exists(cursor, schema_name):
    # Check if the schema exists in the PostgreSQL database
    cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
    return cursor.fetchone() is not None

def read_sql_files_and_create_schema(folder_path, folder_name, db_connection):
    # Read .sql files in the folder
    sql_files = [f for f in os.listdir(folder_path) if f.endswith('.sql') and f.startswith('_pre_dmap')]

    if sql_files:
        print(f"Files in folder '{folder_name}':")
        for sql_file in sql_files:
            print(f"- {sql_file}")

        # Create schema in PostgreSQL with the same name as the folder
        with db_connection.cursor() as cursor:
            schema_name = f'ora2_{folder_name}'
            
            if not schema_exists(cursor, schema_name):
                cursor.execute(f"CREATE SCHEMA {schema_name}")
                print(f"Schema '{schema_name}' created in the database.")
            else:
                print(f"Schema '{schema_name}' already exists in the database.")

        print()

# Example usage:
base_folder_path = r'C:\Users\jerold\Downloads\ora2pg_dump'
unique_folder_names = get_unique_folder_names(base_folder_path)

# Replace these with your PostgreSQL database connection details
db_connection = psycopg2.connect(
    host="local host",
    user="postgres",
    password="root",
    database="Demo"
)

for unique_name in unique_folder_names:
    folder_name = f'ORA2PG_DUMP_{unique_name}'
    folder_path = os.path.join(base_folder_path, folder_name)
    read_sql_files_and_create_schema(folder_path, folder_name, db_connection)

# Close the database connection when done
db_connection.close()





