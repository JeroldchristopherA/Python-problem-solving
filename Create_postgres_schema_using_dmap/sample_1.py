import psycopg2

def execute_sql_file(connection, sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_script = file.read()

    with connection.cursor() as cursor:
        cursor.execute(sql_script)

    connection.commit()

def create_schema(Demo, schema_name, sql_file_path):
    connection_params = {
        'host': 'localhost',
        'port': '5432',
        'user': 'postgres',
        'password': 'root',
        'database': 'Demo'
    }

    try:
        connection = psycopg2.connect(**connection_params)

        # Check if the schema already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = %s", (schema_name,))
            if cursor.fetchone():
                print(f"Schema '{schema_name}' already exists.")
            else:
                # Execute SQL script from file
                execute_sql_file(connection, sql_file_path)
                print(f"Schema '{schema_name}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection:
            connection.close()

# Example usage
database_name = 'Demo'
schema_name = 'your_schema_name'
sql_file_path = 'C:\Users\jerold\Downloads\PostgresSchemas'

create_schema(database_name, schema_name, sql_file_path)
