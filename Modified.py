import os
import re
import subprocess


os.environ['PATH'] += ':C:\Program Files\PostgreSQL\14'
def execute_sql_file(folder_path):
    try:
        sql_file_path = os.path.join(folder_path, 'ora2pg_dump.sql')
        if not os.path.exists(sql_file_path):
            print(f"Error: ora2pg_dump.sql not found in folder '{folder_path}'")
            return False
        with open(sql_file_path, 'r') as sql_file:
            sql_commands = sql_file.read()
        psql_command = f'psql -h localhost -d Demo -U postgres -f {sql_file_path}'
        #psql_command = f'C:\Program Files\PostgreSQL\ 14 \ bin\psql -h localhost -d Demo -U postgres -f {sql_file_path}'

        subprocess.run(psql_command, shell=True)
        print(f"ora2pg_dump.sql executed successfully for folder '{folder_path}'")
        return True
    except Exception as e:
        print(f"Error executing ora2pg_dump.sql for folder '{folder_path}': {e}")
        return False

def main():
    try:
        base_folder_path = r'C:\Users\jerold\Downloads\ora2pg_dump'
        pattern = re.compile(r'ORA2PG_DUMP_(\d+)')
        folders = list(set(match.group(1) for folder in os.listdir(base_folder_path) if (match := pattern.match(folder))))
        for unique_id in folders:
            try:
                folder_path = os.path.join(base_folder_path, f'ORA2PG_DUMP_{unique_id}')
                if not execute_sql_file(folder_path):
                    print(f"Error processing ora2dump.sql in folder '{folder_path}'")

            except Exception as e:
                print(f"Error processing unique folder '{unique_id}': {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
