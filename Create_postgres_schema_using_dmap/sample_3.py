import os
import sqlparse
import psycopg2

def execute_sql(statement, connection):
    with connection.cursor() as cursor:
        cursor.execute(statement)
    connection.commit()

def execute_sql_file(file_path, connection):
    with open(file_path, 'r') as file:
        sql_script = file.read()
    parsed_statements = sqlparse.split(sql_script)
    for statement in parsed_statements:
        if sqlparse.parse(statement)[0].get_type() == 'CREATE':
            execute_sql(statement, connection)
def execute_sql_files_in_directory(directory_path, connection):
    for filename in os.listdir(directory_path):
        if filename.endswith("_dmap.sql"):
            file_path = os.path.join(directory_path, filename)
            execute_sql_file(file_path, connection)
            print(f"DDL statements from '{file_path}' executed successfully.")

try:
    connection = psycopg2.connect(database='Demo',user='postgres',password='root',host='localhost',port='5432')
    sql_files_directory = r'C:\Users\jerold\Downloads\ora2pg_dump\ORA2PG_DUMP_20231115074130'
    execute_sql_files_in_directory(sql_files_directory, connection)
except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        connection.close()
