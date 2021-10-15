from sqlalchemy.engine import create_engine, url
from sqlalchemy.sql.dml import Update
from sqlalchemy.sql.schema import Table, MetaData

installDependencies = input('Do you want to install python packages required to run this script? Yes/No/Y/N ').lower()
if (installDependencies == "yes" or installDependencies == "y"):
    import sys
    import subprocess
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyodbc'])       # Using PyODBC as the DBAPI
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sqlalchemy'])   # SQL Alchemy to make sense of SQL

    # process output with an API in the subprocess module:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
    print(installed_packages)

vincentUsername = input("\nYour username on Vincent: ")
sqlAdminPwd = input("\nPassword for the SQL Servers: ")
serversToUpdate = ['your.server.URL-here.com', 'your.server.URL-is-near.com', 'gme.Power-2-the-Players.com']
for server in serversToUpdate:
    connection_string = "DRIVER={ODBC Driver 17 for SQL Server};"+f"SERVER={server};DATABASE=Vincent;UID=Vincent;PWD={sqlAdminPwd};"
    connection_url = url.URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    print(f"\n{connection_url}\n")
    engine = create_engine(connection_url, echo=True, future=True)
    metadata = MetaData()
    user_table = Table('User', metadata, autoload=True, autoload_with=engine)
    stmts = (Update(user_table).where(user_table.c.Login == vincentUsername).values({"Administrator":1, "Master":1}))
    
    print('Connecting to DB')
    with engine.begin() as conn:
        print(f'\nExecuting update statement for {vincentUsername} on server: {server}')
        print(conn.execute(stmts))

print('\nCongrats! You are now master admin on Master QA / QA Main / FS Sprint')
input('Press any key to exit.')
