ora-1

import os
import re
from os.path import exists

import psycopg2
from sqlalchemy.engine import result

from Utils import pgConnect, Postgres


def Ora2pg_dump_load(self,file_path):
    db_obj = Postgres.PostgresCls(is_oneclick_db=True, schema_name='analytics')
    db_obj.db_connect()
    db_obj_ = Postgres.PostgresCls()
    db_obj_.db_connect()
    try:
        file_path =  r'C:\Users\jerold\Downloads\ora2pg_dump'
        print(file_path)
        folders = [folder for folder in os.listdir(file_path) if
                   os.path.isdir(os.path.join(file_path, folder))]
        print(folders)
        pattern = re.compile(r'ORA2PG_DUMP_(\d+)')
        #db_obj.db_connection = pgConnect.pgConnectCls().test_pg_connection
        db_connection = psycopg2.connect(
            host='localhost',
            database='jerald',
            user='postgres',
            password='root'
        )
        for folder in folders:
            match = pattern.match(folder)
            print(match)
            if match:
                unique_id = match.group(1)
                schema_name = f'ora2_schema_{unique_id}'
                if exists:
                    schema_exists_query = f"SELECT schema_name FROM ora2pg_assessment.schemata WHERE schema_name = '{schema_name}';"
                if not exists:
                    create_schema_query = f"CREATE SCHEMA {schema_name};"
                    with db_obj.db_connection.cursor() as cursor:
                        db_obj.cursor.execute(create_schema_query)
                        db_obj.commit_changes()
                print(f"Schema '{schema_name}' created for folder '{folder}'.")
            else:
                print(f"Schema '{schema_name}' already exists for folder '{folder}'.")
            db_obj.commit_changes()

        db_obj.db_disconnect()
        return {'status': 'success'}

    except Exception as e:
        self.logger.error("Error occurred while processing the Ora2pg_schema details.",
                          extra={"data": {'error': str(e)}})
        result.append({"status": False, "message": "Error occurred while processing the Ora2pg_schema details." + str(e)})
        return result



=====================================================================

ora-2

from flask import Flask, request, jsonify
import psycopg2


from Diff_ora2_dmap import Api_sercive
from Utils import pgConnect

diff_ora2_omap = Flask(__name__)



@diff_ora2_omap.route('/create_db_ora2', methods=['POST'])
def create_database_ora2():
    try:
        connection = pgConnect.pgConnectCls().test_pg_connection
        database_name = request.form['database_name']
        Api_sercive.create_db_postgres(connection, database_name)
        connection.close()
        return f"Database '{database_name}' created successfully."
    except Exception as e:
        return f"Error: {str(e)}"

@diff_ora2_omap.route('/create_schema_ora2', methods=['POST'])
def create_schema():
    try:
        run_ids = request.json.get('run_ids', [])
        connection = Api_sercive.get_postgres_connection()

        response_messages = []
        for run_id in run_ids:
            message = Api_sercive.create_schema_for_run_id(connection, run_id)
            response_messages.append(message)

        return jsonify({"messages": response_messages})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        if connection:
            connection.close()

@diff_ora2_omap.route('/process_dump', methods=['POST'])
def process_dump():
    data = request.json
    run_id = data.get('run_id')
   # Check if the run_id is unique
    if not Api_sercive.is_unique_run_id(run_id, POSTGRES_PATH):
        return jsonify({'error': 'Run ID already exists'}), 400
    # Create dump folder
    dump_folder_path = Api_sercive.create_dump_folder(run_id, POSTGRES_PATH)

    # Create individual schema based on run_id
    Api_sercive.create_schema(run_id, dump_folder_path)

    # Process SQL files in the current dump folder
    Api_sercive.process_sql_files(dump_folder_path)

    return jsonify({'message': 'Dump processed successfully'}), 200



if __name__ == "__main__":
    diff_ora2_omap.run(debug=True)

========================================================

ora-2 api Api_sercive

from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

import os
import pandas as pd
import numpy as np


def schema_exists(connection, schema_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s;",
                    (schema_name,))
        return cursor.fetchone() is not None

def create_schema_for_run_id(connection, run_id):
    schema_name = f"schema_{run_id}"

    if not schema_exists(connection, schema_name):
        with connection.cursor() as cursor:
                cursor.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema_name)))
                connection.commit()
        return f"Schema '{schema_name}' created for run_id {run_id}"
    else:
        return f"Schema '{schema_name}' already exists for run_id {run_id}"


def is_unique_run_id(run_id, base_path):
    dump_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    return f'ORA2PG_DUMP_FOLDER_{run_id}' not in dump_folders

def create_dump_folder(run_id, base_path):
    dump_folder_name = f'ORA2PG_DUMP_FOLDER_{run_id}'
    dump_folder_path = os.path.join(base_path, dump_folder_name)
    os.makedirs(dump_folder_path)
    return dump_folder_path

def create_schema(run_id, dump_folder_path):
    # Replace this with your schema creation logic
    schema_df = pd.DataFrame({'column_name': ['col1', 'col2', 'col3']})
    schema_path = os.path.join(dump_folder_path, 'schema.csv')
    schema_df.to_csv(schema_path, index=False)


def process_sql_files(dump_folder_path):
    # Iterate through .sql files in the specified dump folder
    sql_files = [f for f in os.listdir(dump_folder_path) if f.endswith('.sql')]
    for sql_file in sql_files:
        sql_file_path = os.path.join(dump_folder_path, sql_file)
        with open(sql_file_path, 'r') as file:
            sql_content = file.read()
            # Process SQL content as needed


==========================================================================

ora -3

from flask import Flask, render_template
import os
import re
import pandas as pd
import numpy as np
import psycopg2

app = Flask(__name__)


def extract_unique_name(folder_name):
    match = re.match(r'ORA2PG_DUMP_(\d+)', folder_name)
    if match:
        return match.group(1)
    else:
        return None
def get_unique_folder_names(base_folder_path):
    folders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]
    unique_names = set()
    for folder in folders:
        unique_name = extract_unique_name(folder)
        if unique_name:
            unique_names.add(unique_name)

    return list(unique_names)
def schema_exists(cursor, schema_name):
    cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
    return cursor.fetchone() is not None
def process_unique_folder(base_folder_path, unique_name, db_connection):
    folder_name = f'ORA2PG_DUMP_{unique_name}'
    folder_path = os.path.join(base_folder_path, folder_name)

    sql_files = [f for f in os.listdir(folder_path) if f.endswith('.sql') and f.startswith('ora2pg_dump')]
    if sql_files:
        with db_connection.cursor() as cursor:
            schema_name = f'{folder_name}'
            if not schema_exists(cursor, schema_name):
                cursor.execute(f"CREATE SCHEMA {schema_name}")
    return f"Schema '{schema_name}' created in the database."
@app.route('/')
def index():
    base_folder_path = '/path/to/your/base/folder'
    unique_folder_names = get_unique_folder_names(base_folder_path)
    db_connection = psycopg2.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="your_database"
    )

    results = []

    for unique_name in unique_folder_names:
        result = process_unique_folder(base_folder_path, unique_name, db_connection)
        results.append(result)
    db_connection.close()

   # return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)


============================================================================

ora -4 demo

from flask import Flask, render_template
import os
import re
import psycopg2

app = Flask(__name__)
def extract_unique_name(folder_name):
    match = re.match(r'ORA2PG_DUMP_(\d+)', folder_name)
    if match:
        return match.group(1)
    else:
        return None
def get_unique_folder_names(base_folder_path):
    try:
        folders = [f for f in os.listdir(base_folder_path) if os.path.isdir(os.path.join(base_folder_path, f))]
        unique_names = set()

        for folder in folders:
            unique_name = extract_unique_name(folder)
            if unique_name:
                unique_names.add(unique_name)

        return list(unique_names)
    except Exception as e:
        print(f"Error reading folder names: {e}")
        return []
def create_schema(cursor, schema_name):
    try:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        print(f"Schema '{schema_name}' created in the database.")
    except Exception as e:
        print(f"Error creating schema '{schema_name}': {e}")
def schema_exists(cursor, schema_name):
    try:
        cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error checking if schema '{schema_name}' exists: {e}")
        return False
def read_sql_files_and_insert_data(cursor, folder_path, folder_name):
    try:
        sql_files = [f for f in os.listdir(folder_path) if f.endswith('.sql')]

        if sql_files:
            print(f"Files in folder '{folder_name}':")
            for sql_file in sql_files:
                print(f"- {sql_file}")

                # Insert data into the ora2pg_assessment database (replace with your actual table and data)
                cursor.execute(f"INSERT INTO your_table (schema_name, sql_file) VALUES (%s, %s)",
                               (folder_name, sql_file))
        print()
    except Exception as e:
        print(f"Error reading .sql files in folder '{folder_name}': {e}")





def process_unique_folder(base_folder_path, unique_name, db_connection):
    try:
        folder_name = f'ORA2PG_DUMP_{unique_name}'
        folder_path = os.path.join(base_folder_path, folder_name)
        with db_connection.cursor() as cursor:
            ora2_database = 'Demo'
            cursor.execute(f"CREATE DATABASE {Demos}")
            cursor.execute(f"USE {Demos}")
            schema_name = f'ora2_{folder_name}'
            if not schema_exists(cursor, schema_name):
                create_schema(cursor, schema_name)
                read_sql_files_and_insert_data(cursor, folder_path, folder_name)
        db_connection.commit()
    except Exception as e:
        print(f"Error processing folder '{folder_name}': {e}")
@app.route('/')
def main():
    base_folder_path =  r'C:\Users\jerold\Downloads\ora2pg_dump'
    unique_folder_names = get_unique_folder_names(base_folder_path)
    db_connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="root",
        database="Demo"
    )
    try:
        for unique_name in unique_folder_names:
            process_unique_folder(base_folder_path, unique_name, db_connection)
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        db_connection.close()
    return "Processing completed!"


if __name__ == '__main__':
    app.run(debug=True)
