"""
Server Module
-------------

This module contains the Server class, which is responsible for managing a game server. It handles player connections, queues for solo and duo matches, and ongoing matches. The server facilitates communication between clients, processes game states, and manages match lifecycles.

The Server class uses threading to handle multiple client connections and match processes simultaneously, ensuring smooth gameplay and real-time updates for all connected clients.
"""

import socket
import pickle
import datetime
import pygame
from database.database_query import DBQuery
from _thread import start_new_thread
from configuration_mod import Config
from custom_exceptions import InvalidClientException

from game_objects.player import Player
from game_objects.ball import Ball

from match.elo import Elo
from match.match import Match1v1


class Server:
    """
    Represents a game server for handling player connections and matches.

    Parameters
    ----------
    configuration : Config
        The configuration object for the server.

    Attributes
    ----------
    online_players : set
        Set of ID values of all online players.
    queued_solo_players : set
        Set of ID values of players queued for solo matches.
    queued_duo_players : set
        Set of ID values of players queued for duo matches.
    notify_playing : set
        Set of player IDs to be notified during gameplay.
    matches : list
        List of all ongoing matches.

    Methods
    -------
    __init__(configuration)
        Initializes the Server instance.

    threaded_match()
        Thread function for handling ongoing matches.

    threaded_client(conn)
        Thread function for handling individual client connections.

    create_packet(flag, data)
        Creates a communication packet.

    read_client_message(message)
        Handles client messages and returns a response packet.

    stream_match(message)
        Streams updates during a match to the clients.

    handle_login(d)
        Handles the login process for clients.

    start_server()
        Starts the server and waits for incoming connections.
    """
    online_players = set()       # list of id values of all online players
    queued_solo_players = set()
    queued_duo_players = set()
    notify_playing = set()
    matches = []  # list of all the matches

    def __init__(self, configuration) -> None:
        # TODO: split seperate config for server and client
        self.config = configuration
        # initiate adress
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.server_ip = socket.gethostbyname(self.server)
        # databse connector
        self.db_query = DBQuery(self.config)

        # bind server to the stream
        try:
            self.socket.bind((self.server, self.port))
        except socket.error as socket_error:
            print(str(socket_error))
        self.socket.listen(10)
        print("Waiting for a connection")

    @staticmethod
    def threaded_match(match):
        """
        Continuously run the match loop in a separate thread until the match ends.
        """

        while True:
            end = match.match_loop()
            if end:
                break

    def handle_game_state(self, client_id):
        """
        Handle the game state for a client based on their ID.
        """
        reply = ""
        for match in self.matches:
            if int(client_id) == int(match.p1_id):
                reply = self.create_packet(
                    "game_state_1", [1] + match.share_state())
                self.notify_playing.remove(client_id)
            if int(client_id) == int(match.p2_id):
                reply = self.create_packet(
                    "game_state_1", [2] + match.share_state())
                self.notify_playing.remove(client_id)
        return reply

    def threaded_client(self, conn):
        """
        Manage client-server communication in a separate thread.
        """
        # send client his id
        conn.send(str.encode(str("Welcome, please fill the credentials!")))
        reply = ""
        client_id = "unknown"
        try:
            while True:
                # communication with the client
                # closes when no data is received
                data = conn.recv(2048)
                decoded_data = pickle.loads(data)
                if not data:
                    conn.send(str.encode("Disconnected"))
                    break

                client_id = decoded_data["sender"]

                if client_id in self.notify_playing:
                    reply = self.handle_game_state(client_id)

                else:
                    reply = self.read_client_message(decoded_data)
                conn.sendall(pickle.dumps(reply))
        except (socket.error, pickle.UnpicklingError, EOFError) as exception:
            print(f"Error: {exception}")
        finally:
            # removing client from subscribers after breaking communication
            if client_id in self.online_players:
                self.online_players.remove(client_id)
            if client_id in self.queued_solo_players:
                self.queued_solo_players.remove(client_id)
            if client_id in self.queued_duo_players:
                self.queued_duo_players.remove(client_id)
        print("Connection Closed")
        conn.close()

    @staticmethod
    def create_packet(flag, data):
        """
        Create a data packet with a specific flag and data.
        """
        packet = {"time": datetime.datetime.now(),
                  "sender": "server",
                  "flag": flag,
                  "data": data}
        return packet

    def read_client_message(self, message):
        """
        Process and respond to a client's message based on its flag.
        """
        #default result
        result = None
        # handles the logic of the different packet type
        if message["flag"] == "log_in_data":
            allowed = self.handle_login(message["data"])

            if allowed in ("known user", "registering new user"):
                client_id = self.db_query.get_user_id(message["data"][0])
                if client_id[0] in self.online_players:
                    raise InvalidClientException(
                        "This player is already logged in!")
                self.online_players.add(client_id[0])
                result = self.create_packet("change_of_status", ["online",
                                                                 allowed, client_id[0]])
            else:
                result = self.create_packet("change_of_status",
                                            ["waiting_for_approval", allowed, "uknown"])

        elif message["flag"] == "get_elo":
            user_elo = self.db_query.get_user_elo(message["data"][0])[0]
            top_elo = self.db_query.query_data("top_elo")
            result = self.create_packet("client_elo", [user_elo, top_elo])

        elif message["flag"] == "get_challengers":
            result = self.create_packet("challengers",
                                        self.db_query.query_data("get_challengers"))

        elif message["flag"] == "get_winrate":
            result = self.create_packet("winrate", [
                self.db_query.get_user_winrate(message["data"][0])[0]])

        elif message["flag"] == "get_match_history":
            result = self.create_packet("match_history", [self.db_query.
                                                          get_history(
                                                              message["data"][0]),
                                                          self.db_query.
                                                          get_history(message["data"][0],
                                                                      solo=False)])

        elif message["flag"] == "queued_solo":
            if (len(self.queued_solo_players) >= 1 and
                    (message["sender"]) not in self.queued_solo_players):

                p_1_id = message["sender"]
                p_2_id = self.queued_solo_players.pop()
                p1_name = self.db_query.get_user_name(int(p_1_id))[0]
                p2_name = self.db_query.get_user_name(int(p_2_id))[0]
                player_1 = Player(p1_name, 100, 360, self.config, elo=self.db_query.get_user_elo(
                    p1_name)[0], color="green", server=True)
                player_2 = Player(p2_name, 1180, 360, self.config, elo=self.db_query.get_user_elo(
                    p2_name)[0], color="green", server=True)
                ball = Ball(self.config, server=True)
                new_match = Match1v1(self.config, player_1,
                                     player_2, ball, p_1_id, p_2_id)
                self.matches.append(new_match)
                start_new_thread(self.threaded_match, (new_match, ))
                self.notify_playing.add(int(p_1_id))
                self.notify_playing.add(int(p_2_id))
                result = self.create_packet("Waiting_for_opponent", ["no_data"])
            else:
                self.queued_solo_players.add(int(message["sender"]))
                result = self.create_packet("Waiting_for_opponent", ["no_data"])

        elif message["flag"] == "ingame":
            result = self.stream_match(message)

        return result

    def stream_match(self, message):
        """
        Stream match updates to a client and handle end-game scenarios.
        """
        reply = None
        client_id = message["sender"]

        for match in self.matches:
            if match.playing is False:

                if int(client_id) == int(match.p1_id):
                    reply = self.create_packet(
                        "end_game_state_1", match.get_match_stats())
                    match.p1_end_game_notified = True

                if int(client_id) == int(match.p2_id):
                    reply = self.create_packet(
                        "end_game_state_1", match.get_match_stats())
                    match.p2_end_game_notified = True

                if (match.p2_end_game_notified and match.p1_end_game_notified):
                    # insert match data into db
                    self.db_query.insert_1v1_game(match)

                    # calculate new elo for p1 & p2
                    (p1_new_elo, p2_new_elo) = Elo.calculate_elo(
                        match.p1.elo, match.p2.elo, match.score[0] > match.score[1])

                    # update elo in db for each player
                    self.db_query.update_user_elo(match.p1_id, p1_new_elo)
                    self.db_query.update_user_elo(match.p2_id, p2_new_elo)

                    # update winrate
                    self.db_query.update_user_winrate(
                        match.p1_id, match.p1.name)
                    self.db_query.update_user_winrate(
                        match.p2_id, match.p2.name)
                    self.matches.remove(match)

                return reply

            if int(message["sender"]) == match.p1_id:
                match.p_1_update = message["data"]
                reply = self.create_packet("game_state_1", [1] + match.share_state())
                return reply

            if int(message["sender"]) == match.p2_id:
                match.p_2_update = message["data"]
                reply = self.create_packet("game_state_1", [2] + match.share_state())
                return reply

            return reply

    def handle_login(self, credentials):
        """
        Handle the login process for a client using their credentials.
        """
        allowed = self.db_query.allow_user_credentials(credentials[0], credentials[1])
        return allowed

    def start_server(self):
        """
        Start the server and handle incoming client connections.
        """
        pygame.init()
        while True:
            conn, addr = self.socket.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))


if __name__ == "__main__":
    CONFIG = Config()
    SERVER = Server(CONFIG.config)
    SERVER.start_server()
