import os
import re
import psycopg2


def create_schema(connection, schema_name):
    try:
        create_schema_query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        with connection.cursor() as cursor:
            cursor.execute(create_schema_query)
        connection.commit()
        return True
    except Exception as e:
        print(f"Error occurs while creating schema '{schema_name}': {e}")
        return False

def process_sql_files(folder_path, schema_name):
    try:
        sql_files = [file for file in os.listdir(folder_path) if file.endswith('.sql') and 'pre_dmap' in file]
        for sql_file in sql_files:
            print(f"Processing .sql file '{sql_file}' in folder '{folder_path}' for schema '{schema_name}'")

        return True
    except Exception as e:
        print(f"Error processing .sql files in folder '{folder_path}': {e}")
        return False

def main():
    try:
        base_folder_path =  r'C:\Users\jerold\Downloads\ora2pg_dump'
        pattern = re.compile(r'ORA2PG_DUMP_(\d+)')
        folders = [folder for folder in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, folder))]
        connection = psycopg2.connect( host="localhost", user="postgres", password="root", database="Demo" )
        for folder in folders:
            try:
                match = pattern.match(folder)
                if match:
                    unique_id = match.group(1)
                    schema_name = f'ORA2PG_DUMP_{unique_id}'
                    if create_schema(connection, schema_name):
                        print(f"Schema '{schema_name}' created for folder '{folder}' in the existing database.")
                    else:
                        print(f"Error creating schema '{schema_name}' for folder '{folder}' in the existing database.")
                        print(f"Unique folder name: {unique_id}")
                    folder_path = os.path.join(base_folder_path, folder)
                    if not process_sql_files(folder_path, schema_name):
                        print(f"Error processing .sql files for folder '{folder}'")
            except Exception as e:
                print(f"Error processing folder '{folder}': {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            connection.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

if __name__ == '__main__':
    main()
