import psycopg2
from datetime import datetime
from typing import Dict
class DBQuery:
    """
    Class for handling database queries related to user and match data.

    Parameters
    ----------
    config : dict
        Configuration settings for the database.

    Methods
    -------
    get_user_games(name: str)
        Get the number of games played by a user.
    get_user_won_games(name)
        Get the number of games won by a user.
    get_user_id(name: str)
        Get the ID of a user.
    get_user_name(index: int)
        Get the name of a user.
    get_user_elo(name: str)
        Get the Elo rating of a user.
    get_user_winrate(name: str)
        Get the win rate of a user.
    insert_1v1_game(match: Match1v1)
        Insert a 1v1 match into the database.
    update_user_winrate(idx: int, name: str)
        Update the win rate of a user.
    update_user_elo(idx: int, new_elo: int)
        Update the Elo rating of a user.
    get_history(name: str, solo: bool = True)
        Get the match history of a user.
    query_data(query="user_data")
        Execute a predefined SQL query.
    close_connection_to_db()
        Close the connection to the database.
    create_new_connection()
        Create a new connection to the database.
    allow_user_credentials(username: str, password: str)
        Validate user credentials and handle user registration.
    """
    def __init__(self, config: Dict) -> None:
        self.config = config
        self.database = self.config["database"]["database"]
        self.user = self.config["database"]["user"]
        self.password = self.config["database"]["password"]
        self.host = self.config["database"]["host"]
        self.port = self.config["database"]["port"]
        # Establishing connection the the database
        self.connection = psycopg2.connect(database=self.database,
                                           user=self.user, password=self.password,
                                           host=self.host, port=self.port)
        # Opening cursor to the database
        self.cursor = self.connection.cursor()
        # Basic commands mapping to increase readability
        self.sql_statements = {"user_data": "SELECT * FROM  user_data",
                               "top_elo": """
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
                               "get_challengers": "SELECT Name, Winrate, Elo FROM user_data ORDER BY Elo DESC LIMIT 100"}

    def get_user_games(self, name: str):
        """
        Get the number of games played by a user.

        Parameters
        ----------
        name : str
            The name of the user.

        Returns
        -------
        Tuple
            A tuple containing the result of the query.
        
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        query = "SELECT COUNT(*) AS games_played FROM games_1v1 WHERE (player_1_name = %s OR player_2_name = %s)"
        try:
            self.cursor.execute(query,
                                (name, name))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (name, name))
        result = self.cursor.fetchone()
        self.close_connection_to_db()
        return result

    def get_user_won_games(self, name: str):
        """
        Get the number of games won by a user.

        Parameters
        ----------
        name : str
            The name of the user.

        Returns
        -------
        Tuple
            A tuple containing the result of the query.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        query = "SELECT COUNT(*) AS games_won FROM games_1v1 WHERE (player_1_name = %s AND goals_p1 > goals_p2) OR (player_2_name = %s AND goals_p2 > goals_p1)"
        try:
            self.cursor.execute(query,
                                (name, name))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (name, name))
        result = self.cursor.fetchone()
        self.close_connection_to_db()
        return result

    def get_user_id(self, name: str):
        """
        Get the ID of a user.

        Parameters
        ----------
        name : str
            The name of the user.

        Returns
        -------
        tuple
            A tuple containing the result of the query.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(name, str):
            raise TypeError("Name must be string")
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

    def get_user_name(self, index: int):
        """
        Get the name of a user.

        Parameters
        ----------
        index : int
            The ID of the user.

        Returns
        -------
        Tuple
            A tuple containing the result of the query.
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(index, int):
            raise TypeError("Index must be integer.")
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

    def get_user_elo(self, name: str):
        """
        Get the Elo rating of a user.

        Parameters
        ----------
        name : str
            The name of the user.

        Returns
        -------
        Tuple
            A tuple containing the result of the query.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(name, str):
            raise TypeError("Name must be string")
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

    def get_user_winrate(self, name: str):
        """
        Get the win rate of a user.

        Parameters
        ----------
        name : str
            The name of the user.

        Returns
        -------
        Tuple
            A tuple containing the result of the query.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(name, str):
            raise TypeError("Name must be string")
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

    def insert_1v1_game(self, match):
        """
        Insert a 1v1 match into the database.

        Parameters
        ----------
        match : Match1v1
            The 1v1 match object to be inserted.
        """

        query = """
    INSERT INTO games_1v1 (player_1_name, player_2_name, player_1_elo, player_2_elo, goals_p1, goals_p2, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
        try:
            self.cursor.execute(query,
                                (match.p1.name, match.p2.name, match.p1.elo, match.p2.elo, match.score[0], match.score[1], datetime.now()))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (match.p1.name, match.p2.name, match.p1.elo, match.p2.elo, match.score[0], match.score[1], datetime.now()))
        self.connection.commit()
        self.close_connection_to_db()

    def update_user_winrate(self, idx: int, name: str):
        """
        Update the win rate of a user.

        Parameters
        ----------
        idx : int
            The ID of the user.
        name : str
            The name of the user.

        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        if not isinstance(idx, int):
            raise TypeError("Idx must be integer.")
        query = "UPDATE user_data SET winrate = %s WHERE id = %s"

        # calculate winrate
        games_won = self.get_user_won_games(name)[0]
        games_played = self.get_user_games(name)[0]

        winrate = (games_won // games_played) * 100

        try:
            self.cursor.execute(query,
                                (winrate, idx,))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(query,
                                (winrate, idx,))
        self.connection.commit()
        self.close_connection_to_db()

    def update_user_elo(self, idx: int, new_elo: int):
        """
        Update the Elo rating of a user.

        Parameters
        ----------
        idx : int
            The ID of the user.
        new_elo : int
            The new Elo rating.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(new_elo, int):
            raise TypeError("New_elo must be integer.")
        if not isinstance(idx, int):
            raise TypeError("Idx must be integer.")
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

    def get_history(self, name: str, solo: bool = True):
        """
        Get the match history of a user.

        Parameters
        ----------
        name : str
            The name of the user.
        solo : bool, optional
            True for solo matches, False for team matches. Defaults to True.

        Returns
        -------
        List
            A list containing the result of the query.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        if not isinstance(solo, bool):
            raise TypeError("Solo must be bool.")
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

    def query_data(self, query: str = "user_data"):
        """
        Execute a predefined SQL query.

        Parameters
        ----------
        query : str, optional
            The key of the predefined SQL query. Defaults to "user_data".

        Returns
        -------
        List
            A list containing the result of the query.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(query, str):
            raise TypeError("Query must be string")

        try:
            self.cursor.execute(self.sql_statements.get(query))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(self.sql_statements.get(query))
        result = self.cursor.fetchall()
        self.close_connection_to_db()
        return result

    def close_connection_to_db(self):
        """
        Close the connection to the database.
        """
        self.cursor.close()
        self.connection.close()

    def create_new_connection(self):
        """Establishes a new connection to the database 
        
        Raises
        ------
        ConnectionError
            When failing to connect to database.
        """
        try:
            self.connection = psycopg2.connect(database=self.database,
                                            user=self.user, password=self.password,
                                            host=self.host, port=self.port)
            # Opening cursor to the database
            self.cursor = self.connection.cursor()
        except:
            raise ConnectionError("Failed to connect to the database make sure it is running")

    def allow_user_credentials(self, username: str, password: str):
        """
        Validate user credentials and handle user registration.

        Parameters
        ----------
        username : str
            The username provided by the user.
        password : str
            The password provided by the user.

        Returns
        -------
        str
            A string indicating the result of the validation/registration process.
            
        Raises
        ------
        TypeError
            When inputs of incorrect type are provided
        """
        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError("Both username and password must be strings.")
        if username == "" or password == "":
            return "Make sure to fill both name and password"

        # Execute a query to retrieve user credentials
        try:
            self.cursor.execute(
                "SELECT Name, Password FROM user_data WHERE Name = %s", (username,))
        except psycopg2.InterfaceError:
            self.create_new_connection()
            self.cursor.execute(
                "SELECT Name, Password FROM user_data WHERE Name = %s", (username,))
        user_data = self.cursor.fetchone()
        if user_data is not None and user_data[1] == password:
            # The username is present and the password is correct ->client will be linked to that existing account
            self.close_connection_to_db()
            return "known user"
        if user_data is not None and user_data[1] != password:
            # existing username but wrong password
            self.close_connection_to_db()
            return "Incorrect password for this username"
        # Creating new user in the database and inserting him into the database
        self.cursor.execute("INSERT INTO user_data (Name, Password, Elo, Winrate, Skin) VALUES(%s, %s, %s, %s, %s)",
                            (username, password, 1000, 0, "Skin1"))
        self.connection.commit()
        self.close_connection_to_db()
        return "registering new user"
