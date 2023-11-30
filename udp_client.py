import socket
import ipaddress
from packet import Packet
from Http import *

def sendToServer(host, port, request, routerHost, routerPort):
    # Convert host name to IP address
    peer_ip = ipaddress.ip_address(socket.gethostbyname(host))
    
    # Create a UDP socket
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    timeout = 10  # Timeout for receiving responses
    max_payload_size = 1013  # Maximum payload size per packet
    seq_num = 1  # Starting sequence number for packets

    try:
        # Splitting the request into smaller chunks if it's too large
        chunks = [request[i:i + max_payload_size] for i in range(0, len(request), max_payload_size)]
        print(f"Number of packets to send: {len(chunks)}")

        # Send each chunk as a separate packet
        for chunk in chunks:
            print(f"Sending packet {seq_num} to {host}:{port}")
            p = Packet(packet_type=0, seq_num=seq_num, peer_ip_addr=peer_ip, peer_port=8007, payload=chunk)
            conn.sendto(p.to_bytes(), (routerHost, routerPort))
            seq_num += 1  # Incrementing sequence number for next packet

        # Set a timeout for the socket to receive responses
        conn.settimeout(timeout)

        # Receiving responses
        all_responses = b''
        while True:
            # try:
                print("Waiting for response...")
                response, sender = conn.recvfrom(1024)
                print(f"Received response from {sender}")

                # Convert the response to a Packet object
                p = Packet.from_bytes(response)
                print(p)

                # Check for a condition to break the loop
                # This could be an empty payload or a special packet indicating the end
                if p.payload.decode("utf-8") == "end":
                    print("No more data to receive.")
                    break

                # Concatenate the received payload to form the complete response
                all_responses += p.payload

            # except socket.timeout:
            #     print(f"No response received after {timeout}s")
            #     break

        # Print the final combined response
        print("The combined response is:\n", all_responses.decode("utf-8"))


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Closing the socket
        conn.close()
        print("Socket closed.")

# # Usage Example
# host = "localhost"
# port = 41830

# # For a GET request (assuming getHTTP() returns a bytes object)
# request = getHTTP(host, port, "/test.txt", None, None, False)
# print("HTTP GET Request:", request)
# response = sendToServer(host, port, request)

# For a POST request (similar to GET, assuming postHTTP() returns a bytes object)
# request = postHTTP(host, port, "/path", params={}, filepath=None, headers={}, verbose=False)
# response = udp_client(host, port, request)
