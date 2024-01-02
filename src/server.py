import socket
import sys
import pickle
import datetime
from database.database_query import DBQuery
from _thread import *
from configuration_mod import Config



class Server:
    online_players = []         # list of id values of all online players
    available_players = []  # list of id values of all online players
    #waiting for a match queued
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
    def threaded_client(self, conn):
        #send client his id
        conn.send(str.encode(str("Welcome, please fill the credentials!")))
        reply = ""
        while True:
            try:
                #communication with the client
                #closes when no data is received
                data = conn.recv(2048)
                decoded_data = pickle.loads(data)
                if not data:
                    conn.send(str.encode("Disconnected"))
                    break
                else:
                    print(decoded_data)
                    reply = self.read_client_message(decoded_data)
                conn.sendall(pickle.dumps(reply))
            except Exception as e :
                print(e)
                break

        print("Connection Closed")
        conn.close()
        
    def create_packet(self, flag, data):
        packet = {"time":datetime.datetime.now(),
        "sender":"server", 
        "flag":flag,
        "data":data}
        print(packet)
        return packet
    def read_client_message(self, message):
        #handles the logic of the different packet type
        if message["flag"] == "log_in_data":
            allowed = self.handle_login(message["data"])
            if allowed in ("known user", "registering new user"):
                client_id = self.db_query.get_user_id(message["data"][0])
                self.online_players.append(client_id[0])
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
    def handle_login(self, d):
        allowed = self.db_query.allow_user_credentials(d[0], d[1])
        return allowed
    
    def start_server(self):
        while True:
            conn, addr = self.s.accept()
            print("Connected to: ", addr)

            start_new_thread(self.threaded_client, (conn,))


if __name__ == "__main__":
    config= Config()
    server = Server(config.config)
    server.start_server()
