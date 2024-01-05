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
        self.sql_statements = {"user_data":"SELECT * FROM  user_data",
                               "top_elo":"""
(
  SELECT Elo
  FROM user_data
  ORDER BY Elo DESC
  LIMIT 1 OFFSET 99
)
UNION
(
  SELECT Elo
  FROM user_data
  ORDER BY Elo ASC
  LIMIT 1
);
""",
                               "get_challengers":"SELECT Name, Winrate, Elo FROM user_data ORDER BY Elo DESC LIMIT 100"}
        
    def get_user_id(self, name):
        query = "SELECT id FROM user_data WHERE Name =%s"
        try:
            self.cursor.execute(query,
                                (name,))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (name,))
        result = self.cursor.fetchone()
        self.close_connection_to_db()
        return result
    
    def get_user_name(self, index):
        query = "SELECT Name FROM user_data WHERE id =%s"
        try:
            self.cursor.execute(query,
                                (index,))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (index,))
        result = self.cursor.fetchone()
        self.close_connection_to_db()
        return result

    def get_user_elo(self, name):
        query = "SELECT Elo FROM user_data WHERE Name =%s"
        try:
            self.cursor.execute(query,
                                (name,))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (name,))
        result = self.cursor.fetchone()
        self.close_connection_to_db()
        return result

    def get_user_winrate(self, name):
        query = "SELECT Winrate FROM user_data WHERE Name =%s"
        try:
            self.cursor.execute(query,
                                (name,))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (name,))
        result = self.cursor.fetchone()
        self.close_connection_to_db()
        return result

    def update_user_elo(self, idx, new_elo):
        query = "UPDATE user_data SET elo = %s WHERE id = %s"
        try:
            self.cursor.execute(query,
                                (new_elo, idx, ))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (new_elo, idx,))    
        self.connection.commit()
        self.close_connection_to_db()

    def get_history(self, name, solo = True):
        if solo:
            query = "SELECT * FROM games_1v1 WHERE Player_1_name = %s OR Player_2_name = %s ORDER BY Date DESC LIMIT 10"
            try:
                self.cursor.execute(query,
                                    (name, name,))
            except psycopg2.InterfaceError:
                self.create_new_connection()
                self.cursor.execute(query,
                                    (name, name,))
        else:
            query = "SELECT * FROM games_2v2 WHERE Player_1_name = %s OR Player_2_name = %s OR Player_3_name = %s OR Player_4_name = %s ORDER BY Date DESC LIMIT 10"
            try:
                self.cursor.execute(query,
                                    (name, name, name, name))
            except psycopg2.InterfaceError:
                self.create_new_connection()
                self.cursor.execute(query,
                                    (name, name, name, name))
        result = self.cursor.fetchall()
        self.close_connection_to_db()
        return result
    
    def query_data(self, query = "user_data"):
        """_summary_

        Args:
            query (str, optional): _description_. Defaults to "users".
        """
        try:
            self.cursor.execute(self.sql_statements.get(query))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(self.sql_statements.get(query))
        result = self.cursor.fetchall()
        self.close_connection_to_db()
        return result

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
        #TODO: If time allows, hash passwords in the database and compare hashes
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
        self.cursor.execute("INSERT INTO user_data (Name, Password, Elo, Winrate, Skin) VALUES(%s, %s, %s, %s, %s)",
                    (username, password,1000,1000,"Skin1"))
        self.connection.commit()
        self.close_connection_to_db()
        return "registering new user"
            
        
