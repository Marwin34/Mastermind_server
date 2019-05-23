import selectors
import socket
import message_util


class ComSupervisor:
    def __init__(self, addr, port, players_container):
        self.selector = selectors.DefaultSelector()

        self.port = port
        self.addr = addr
        self.socket = socket.socket()
        self.socket.bind((self.addr, self.port))
        self.socket.listen(100)
        self.socket.setblocking(False)

        self.selector.register(self.socket, selectors.EVENT_READ, self.accept)

        self.players_container = players_container

    def accept(self, sock, mask):
        conn, addr = sock.accept()

        player = {
            'conn': conn,
            'addr': addr,
            'requests': [],
            'responses': [],
            'nick': "",
            'to_remove': False,
            'table': None
        }

        if not self.players_list_contains(player):
            conn.setblocking(False)
            self.players_container.append(player)
            print("Accepted", conn, "from", addr, "added", player)
            self.selector.register(conn, selectors.EVENT_READ, self.read)
        else:
            print("Connection already accepted.")

    def read(self, conn, mask): # callback function for self.selector.register()
        received, data = message_util.recv_msg(conn)
        if received and data:
            self.fetch_data(conn, data)
        elif not received:
            self.remove_player(conn)
    # message_util.send_msg(conn, data)

    def send(self):
        for player in self.players_container:
            if player['responses']:
                for response in player['responses']:
                    message_util.send_msg(player['conn'], response)
                player['responses'] = []

    def fetch_events(self):
        events = self.selector.select(0)  # 0 timeout == non blocking select
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)

    def players_list_contains(self, player):
        for entry in self.players_container:
            if entry['conn'] == player['conn']:
                return True

        return False

    def fetch_data(self, conn, data):
        for player in self.players_container:
            if player['conn'] == conn:
                player['requests'].append(data)

    def remove_player(self, conn):
        for key, value in enumerate(self.players_container):
            if value['conn'] == conn:
                self.players_container.remove(value)
        self.selector.unregister(conn)
        conn.close()

    def clean(self):
        for player in self.players_container:
            if player['to_remove']:
                self.players_container.remove(player)
                self.selector.unregister(player['conn'])
                player['conn'].close()
