import os
import subprocess

# Replace with your actual PostgreSQL server details
database_name = 'Checking'
user = 'postgres'
password = 'root'
host = 'localhost'
port = '5432'

# Specify the directory containing _damp.sql files
directory_path = r'C:\Users\jerold\Downloads\ora2pg_dump\ORA2PG_DUMP_20231115074117'

def execute_sql_file(file_path):
    # Use subprocess to run psql and execute the SQL script
    psql_command = f'psql -h {host} -p {port} -U {user} -d {database_name} -f "{file_path}"'
    process = subprocess.run(psql_command, shell=True)

    if process.returncode == 0:
        print(f"SQL script from '{file_path}' executed successfully.")
    else:
        print(f"Error executing SQL script from '{file_path}': {process.stderr.decode(errors='replace')}")

# Iterate through all files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith("_damp.sql"):
        file_path = os.path.join(directory_path, filename)
        execute_sql_file(file_path)
