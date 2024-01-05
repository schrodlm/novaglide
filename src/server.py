import socket
import pickle
import datetime
import pygame
from database.database_query import DBQuery
from _thread import start_new_thread
from configuration_mod import Config
from match.match import Match1v1
from game_objects.player import Player
from game_objects.ball import Ball

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

    handle_playing()
        Handles ongoing matches and removes completed ones.

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
    matches = []        #list of all the matches       
    def __init__(self, configuration) -> None:
        #TODO: split seperate config for server and client
        self.config = configuration
        #initiate adress
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.server_ip = socket.gethostbyname(self.server)
        #databse connector
        self.db_query = DBQuery(self.config)
        #bind server to the stream
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
        self.s.listen(10)
        print("Waiting for a connection")
        
    def threaded_match(self, match):
        while True:
            end = match.match_loop()
            if end:
                #TODO: send notification to the clients
                try:
                    self.matches.remove(match)
                except ValueError:
                    print("match already removed")
                print("Curent matches: ", self.matches)
                break
    def threaded_client(self, conn):
        #send client his id
        conn.send(str.encode(str("Welcome, please fill the credentials!")))
        #TODO: maybe change reply to soemthing that can be pickled
        reply = ""
        client_id = "unknown"
        try:
            while True:
                #communication with the client
                #closes when no data is received
                data = conn.recv(2048)
                decoded_data = pickle.loads(data)
                if not data:
                    conn.send(str.encode("Disconnected"))
                    break
                else:
                    client_id = decoded_data["sender"]
                    if client_id in self.notify_playing: 
                        for match in self.matches:
                            if int(client_id) == int(match.p1_id):
                                reply = self.create_packet("game_state_1",[1] + match.share_state())
                                self.notify_playing.remove(client_id)
                            if int(client_id) == int(match.p2_id):
                                reply = self.create_packet("game_state_1",[2] + match.share_state())
                                self.notify_playing.remove(client_id)
                    else:
                        reply = self.read_client_message(decoded_data)
                conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
        finally:
            #removing client from subscribers after breaking communication
            if client_id in self.online_players:
                self.online_players.remove(client_id)
            if client_id in self.queued_solo_players:
                self.queued_solo_players.remove(client_id)
            if client_id in self.queued_duo_players:
                self.queued_duo_players.remove(client_id)
        print("Connection Closed")
        conn.close()
        
    def create_packet(self, flag, data):
        packet = {"time":datetime.datetime.now(),
        "sender":"server", 
        "flag":flag,
        "data":data}
        return packet
    def read_client_message(self, message):
        #handles the logic of the different packet type
        if message["flag"] == "log_in_data":
            allowed = self.handle_login(message["data"])

            if allowed in ("known user", "registering new user"):
                client_id = self.db_query.get_user_id(message["data"][0])
                self.online_players.add(client_id[0])
                return self.create_packet("change_of_status", ["online",
                allowed, client_id[0]])
            else:
                return self.create_packet("change_of_status",
                                    ["waiting_for_approval", allowed,"uknown"])

        if message["flag"] == "get_elo":
            return self.create_packet("client_elo",[self.db_query.get_user_elo(message["data"][0])[0],
                                                    self.db_query.query_data("top_elo")[0][0]])

        if message["flag"] == "get_challengers":
            return self.create_packet("challengers",
            self.db_query.query_data("get_challengers"))

        if message["flag"] == "get_winrate":
            return self.create_packet("winrate",[
            self.db_query.get_user_winrate(message["data"][0])[0]])
            
        if message["flag"] == "get_match_history":
            return self.create_packet("match_history",[self.db_query.
                                        get_history(message["data"][0]),
                                        self.db_query.
                                        get_history(message["data"][0],
                                        solo=False)])

        if message["flag"] == "queued_solo":
            if len(self.queued_solo_players) >= 1 and (message["sender"]) not in self.queued_solo_players:
                p_1_id = message["sender"]
                p_2_id = self.queued_solo_players.pop()
                player_1 = Player(self.db_query.get_user_name(int(p_1_id))[0], 100,360,self.config, color = "green",server=True)
                player_2 = Player(self.db_query.get_user_name(int(p_2_id))[0], 1180,360,self.config, color = "green",server=True)
                ball = Ball(self.config,server=True)
                new_match = Match1v1(self.config, player_1, player_2, ball, p_1_id, p_2_id)
                self.matches.append(new_match)
                start_new_thread(self.threaded_match, (new_match, ))
                self.notify_playing.add(int(p_1_id))
                self.notify_playing.add(int(p_2_id))
                return self.create_packet("Waiting_for_opponent",["no_data"])
            else:
                self.queued_solo_players.add(int(message["sender"]))
                return self.create_packet("Waiting_for_opponent",["no_data"])
        if message["flag"] == "ingame":
            return self.stream_match(message)

    def stream_match(self, message):
        for match in self.matches:
            if int(message["sender"]) == match.p1_id:
                match.p_1_update = message["data"]
                return self.create_packet("game_state_1",[1] + match.share_state())
            elif int(message["sender"]) == match.p2_id:
                match.p_2_update = message["data"]
                return self.create_packet("game_state_1",[2] + match.share_state())
        
    def handle_login(self, d):
        allowed = self.db_query.allow_user_credentials(d[0], d[1])
        return allowed
    
    def start_server(self):
        pygame.init()
        while True:
            conn, addr = self.s.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))


if __name__ == "__main__":
    config= Config()
    server = Server(config.config)
    server.start_server()
