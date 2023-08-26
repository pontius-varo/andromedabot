from sqlite3 import Error, connect

def create_connection(path):
    connection = None
    try:
        connection = connect(path)
        print("Connection to Database established.")
    except Error as e:
        print("The error \'{e}\' occurred. Are you sure that the db file exists?")
        return

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occured")