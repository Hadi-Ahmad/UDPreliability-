import argparse
import socket
import re
import ipaddress
from server import serverRun
from packet import Packet


def extract_ip_and_port(input_string):
    pattern = r'peer=(\d+\.\d+\.\d+\.\d+):(\d+)'
    match = re.search(pattern, input_string)
    
    if match:
        ip_address = match.group(1)
        port = match.group(2)
        return ip_address, port
    else:
        return None, None
    

def recieveFromClient(port):
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        conn.bind(('', port))
        print('Echo server is listening at', port)
        while True:
            data, sender = conn.recvfrom(1024)
            
            # Create Packet object from received data
            packet = Packet.from_bytes(data)

            p = Packet.__repr__(packet)
            ip_adress, finalPort = extract_ip_and_port(p)
            peer_ip = ipaddress.ip_address(socket.gethostbyname(ip_adress))

            # Extract payload from the packet
            http_request = packet.payload.decode('utf-8')
            # print("Extracted HTTP request:\n", http_request)

            # Process the HTTP request
            response = serverRun('data', http_request)
            # print("Generated response:\n", response)

            # Send response back to the client
            sendToClient(conn, response, sender, peer_ip, finalPort)


    finally:
        conn.close()

def sendToClient(conn, data, sender, givenAddress, givenPort):
    try:
        # Placeholder for your response generation logic
        response = data  
        # print("The response is:\n", response)

        # Splitting the response into chunks if it's too large
        max_payload_size = 1013  # Max payload size
        chunks = [response[i:i + max_payload_size] for i in range(0, len(response), max_payload_size)]

        # Send each chunk as a separate packet
        for index, chunk in enumerate(chunks):
            # Encode the chunk to get its byte size
            encoded_chunk = chunk.encode('utf-8')

            # Convert raw data to Packet object
            p = Packet.from_bytes(chunk.encode("utf-8"))
            
            # Create a new packet with the chunk as payload
            response_packet = Packet(packet_type=p.packet_type,
                                     seq_num=p.seq_num,
                                     peer_ip_addr=givenAddress,
                                     peer_port=givenPort,
                                     payload=encoded_chunk)
            
            endpayload = "end".encode("utf-8")
            end_packet = Packet(packet_type=p.packet_type,
                            seq_num=p.seq_num,
                            peer_ip_addr=givenAddress,
                            peer_port=givenPort,
                            payload=endpayload)

            # Print the size of the payload for this chunk
            print(f"Sending packet {index + 1} to {sender} with payload size: {len(encoded_chunk)} bytes")

            conn.sendto(response_packet.to_bytes(), sender)
            conn.sendto(end_packet.to_bytes(), sender) #1 Packet indicating the respinse is sent

    except Exception as e:
        print("Error: ", e)




# Usage python udp_server.py [--port port-number]
parser = argparse.ArgumentParser()
parser.add_argument("--port", help="echo server port", type=int, default=8007)
args = parser.parse_args()
recieveFromClient(args.port)
