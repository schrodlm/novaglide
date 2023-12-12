import psycopg2

class DBQuery:
    def __init__(self,config) -> None:
        self.config = config
        self.database = self.config["database"]["database"]
        self.user = self.config["database"]["user"]
        self.password = self.config["database"]["password"]
        self.host = self.config["database"]["host"]
        self.port = self.config["database"]["port"]
        #Establishing connection the the database
        self.connection = psycopg2.connect(database = self.database,
                user = self.user, password = self.password,
                host = self.host, port = self.port)
        #Opening cursor to the database
        self.cursor = self.connection.cursor()
        #Basic commands mapping to increase readability
        self.sql_statements = {"user_data":"SELECT * FROM  user_data"}
        self.data = None
    def query_data(self, query = "user_data"):
        """_summary_

        Args:
            query (str, optional): _description_. Defaults to "users".
        """
        self.cursor.execute(self.sql_statements.get(query))
        self.data = self.cursor.fetchall()
        self.close_connection_to_db()

    def close_connection_to_db(self):
        """_summary_
        """
        self.cursor.close()
        self.connection.close()
        
    def create_new_connection(self):
        """Establishes new connection to the database 
        """
        self.connection = psycopg2.connect(database = self.database,
                user = self.user, password = self.password,
                host = self.host, port = self.port)
        #Opening cursor to the database
        self.cursor = self.connection.cursor()
    
    def allow_user_credentials(self, username, password):
        #Force the user to always fill both of the fields
        if username == "" or password == "":
            return "Make sure to fill both name and password"
        
        # Execute a query to retrieve user credentials
        try:
            self.cursor.execute("SELECT Name, Password FROM user_data WHERE Name = %s", (username,))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute("SELECT Name, Password FROM user_data WHERE Name = %s", (username,))
        user_data = self.cursor.fetchone()
        if user_data is not None and user_data[1] == password:
            #The username is present and the password is correct ->client will be linked to that existing account
            self.close_connection_to_db()
            return "known user"
        if user_data is not None and user_data[1] != password:
            #existing username but wrong password
            self.close_connection_to_db()
            return "Incorrect password for this username"
        #Creating new user in the database and inserting him into the database
        self.cursor.execute("INSERT INTO user_data (Name, Password, Elo_1v1, Elo_2v2, Skin) VALUES(%s, %s, %s, %s, %s)",
                    (username, password,1000,1000,"Skin1"))
        self.connection.commit()
        self.close_connection_to_db()
        return "registering new user"
            
        
