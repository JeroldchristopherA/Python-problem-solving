# #from flask import Flask, jsonify
# import os
# import re
# import psycopg2
# from psycopg2 import sql

# #app = Flask(__name__)

# def create_database():
#     try:
#         # Connect to PostgreSQL and create a database
#         connection = psycopg2.connect(
#             host='your_host',
#             database='your_database',
#             user='your_user',
#             password='your_password'
#         )

#         create_db_query = "CREATE DATABASE ora2pg_assessment;"
#         with connection.cursor() as cursor:
#             cursor.execute(create_db_query)

#         connection.commit()
#         connection.close()
#         return True
#     except Exception as e:
#         print(f"Error creating database: {e}")
#         return False

# # ... (previous code)

# def create_schema(schema_name):
#     try:
#         connection = psycopg2.connect(
#             host='your_host',
#             database='ora2pg_assessment',
#             user='your_user',
#             password='your_password'
#         )

#         create_schema_query = sql.SQL("CREATE SCHEMA IF NOT EXISTS {};").format(sql.Identifier(schema_name))
#         with connection.cursor() as cursor:
#             cursor.execute(create_schema_query)

#         connection.commit()
#         connection.close()
#         return True
#     except Exception as e:
#         print(f"Error creating schema '{schema_name}': {e}")
#         return False

# def process_sql_files(folder_path, schema_name):
#     try:
#         connection = psycopg2.connect(
#             host='your_host',
#             database='ora2pg_assessment',
#             user='your_user',
#             password='your_password'
#         )

#         sql_files = [file for file in os.listdir(folder_path) if file.endswith('.sql') and 'pre_dmap' in file]
#         for sql_file in sql_files:
#             sql_file_path = os.path.join(folder_path, sql_file)
            
#             # Read SQL file content
#             with open(sql_file_path, 'r') as sql_file_content:
#                 sql_query = sql_file_content.read()
#                 print(f"Processing .sql file '{sql_file}' in folder '{folder_path}' for schema '{schema_name}':\n{sql_query}")

#                 # Execute the SQL query
#                 with connection.cursor() as cursor:
#                     cursor.execute(sql_query)

#         connection.commit()
#         connection.close()

#         return True
#     except Exception as e:
#         print(f"Error processing .sql files in folder '{folder_path}': {e}")
#         return False

# # ... (remaining code)


# @app.route('/process_folders', methods=['GET'])
# def process_folders():
#     try:
#         base_folder_path = '/path/to/base/folder'
#         pattern = re.compile(r'ORA2PG_DUMP_FOLDER_(\d+)')
#         folders = [folder for folder in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, folder))]

#         # Create ora2pg_assessment database if it doesn't exist
#         if not create_database():
#             return jsonify({"error": "Error creating ora2pg_assessment database."})

#         for folder in folders:
#             try:
#                 match = pattern.match(folder)

#                 if match:
#                     unique_id = match.group(1)
#                     schema_name = f'ora2_schema_{unique_id}'

#                     # Create schema in ora2pg_assessment database
#                     if create_schema(schema_name):
#                         print(f"Schema '{schema_name}' created for folder '{folder}' in ora2pg_assessment database.")
#                     else:
#                         print(f"Error creating schema '{schema_name}' for folder '{folder}' in ora2pg_assessment database.")

#                     # Iterate through .sql files in the unique folder
#                     folder_path = os.path.join(base_folder_path, folder)
#                     if not process_sql_files(folder_path, schema_name):
#                         return jsonify({"error": f"Error processing .sql files for folder '{folder}'"})

#             except Exception as e:
#                 return jsonify({"error": f"Error processing folder '{folder}': {e}"})

#         return jsonify({"status": "Folders processed successfully!"})

#     except Exception as e:
#         return jsonify({"error": f"Error: {e}"})

# if __name__ == '__main__':
#     app.run(debug=True)




import os
import re
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

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
@app.route('/api/data', methods=['GET'])
def get_api_data():
    try:
        base_folder_path = r'C:\Users\jerold\Downloads\ora2pg_dump'
        pattern = re.compile(r'ORA2PG_DUMP_(\d+)')
        folders = [folder for folder in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, folder))]
        connection = psycopg2.connect(host="localhost", user="postgres", password="root", database="Demo")
        for folder in folders:
            try:
                match = pattern.match(folder)
                if match :
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
        return jsonify({"message": "API data processed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            connection.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")

if __name__ == '__main__':
    app.run(debug=True)



