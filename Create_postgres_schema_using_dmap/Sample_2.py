import os
import psycopg2

def execute_sql_from_file(connection, filename):
    with open(filename, 'r') as file:
        sql_script = file.read()

    with connection.cursor() as cursor:
        cursor.execute(sql_script)
    connection.commit()

def run_sql_files_in_psql(database_name, sql_files_folder):
    connection_params = {
         'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': 'root',
        'database': 'Demo'
    }

    try:
        connection = psycopg2.connect(**connection_params)

        for sql_file in os.listdir(sql_files_folder):
            if sql_file.endswith(".sql"):
                sql_file_path = os.path.join(sql_files_folder, sql_file)

                print(f"Executing SQL statements from: {sql_file}")
                execute_sql_from_file(connection, sql_file_path)

        print("All SQL files executed successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

# Example usage
database_name = 'Demo'
sql_files_folder = r'C:\Users\jerold\Downloads\PostgresSchemas'
run_sql_files_in_psql(database_name, sql_files_folder)
