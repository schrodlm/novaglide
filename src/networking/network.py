"""Network Module

This module provides a simple Network class for handling socket communication.

Classes:
    Network: A class for managing socket communication.
"""
import pickle
import socket


class Network:
    """Network Class

    Represents a network connection using sockets.

    Attributes
    ----------
    client : socket.socket
        The socket object for communication.
    host : str
        The host address to connect to.
    port : int
        The port number for the connection.
    addr : tuple
        A tuple containing the host and port (host, port).

    Methods
    -------
    __init__():
        Initializes a new Network instance.
    connect():
        Connects to the specified host and port.
    send(data: str) -> str:
        Sends data over the socket and receives a response.
    """

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "localhost"
        self.port = 5555
        self.addr = (self.host, self.port)

    def connect(self):
        """Connect to the specified host and port.

        Returns
        -------
        str
            A message indicating the status of the connection.
        """
        self.client.connect(self.addr)
        return self.client.recv(2048).decode()

    def send(self, data):
        """Send data over the socket and receive a response.

        Parameters
        ----------
        data : obj any
            The data to be sent over the socket.

        Returns
        -------
        obj any
            The response received from the server.

        Raises
        ------
        socket.error
            If an error occurs during socket communication.
        """
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(2048))
            return reply
        except socket.error as e:
            return str(e)
