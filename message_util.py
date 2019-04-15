import json
import struct


# server version uses connection instead of socket
def send_msg(conn, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = json.dumps(msg, ensure_ascii=False).encode('utf-8')
    msg = struct.pack('>I', len(msg)) + msg
    conn.sendall(msg)


def recv_msg(conn):
    # Read message length and unpack it into an integer
    received, raw_msglen = recv_all(conn, 4)
    if not received and not raw_msglen:
        return (False, None)

    msglen = struct.unpack('>I', raw_msglen)[0]

    # Read the message data
    received, coded_data = recv_all(conn, msglen)
    if not received:
        return (False, None)

    return (True, json.loads(coded_data, encoding='utf-8'))


def recv_all(conn, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        try:
            packet = conn.recv(n - len(data))
        except ConnectionResetError:
            return (False, [])
        if not packet:
            return None
        data += packet
    return (True, data)
