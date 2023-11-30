from packet import Packet

def udp_handshakeClient(conn, host, port, peer_ip):
    # Step 1: Send SYN
    print("Sending SYN...")
    syn_packet = Packet(packet_type=1, seq_num=1, peer_ip_addr=peer_ip, peer_port=port, payload=b'SYN')
    conn.sendto(syn_packet.to_bytes(), (host, port))

    # Step 2: Wait for SYN-ACK
    response, _ = conn.recvfrom(1024)
    syn_ack_packet = Packet.from_bytes(response)
    if syn_ack_packet.payload == b'SYN-ACK':
        print("Received SYN-ACK, sending ACK...")

        # Step 3: Send ACK
        ack_packet = Packet(packet_type=2, seq_num=2, peer_ip_addr=peer_ip, peer_port=port, payload=b'ACK')
        conn.sendto(ack_packet.to_bytes(), (host, port))
        print("Handshake completed.")

def udp_handshakeServer(conn, sender):
    # Expect SYN
    data, _ = conn.recvfrom(1024)
    syn_packet = Packet.from_bytes(data)
    if syn_packet.payload == b'SYN':
        print("Received SYN, sending SYN-ACK...")

        # Send SYN-ACK
        syn_ack_packet = Packet(packet_type=1, seq_num=1, peer_ip_addr=syn_packet.peer_ip_addr, peer_port=syn_packet.peer_port, payload=b'SYN-ACK')
        conn.sendto(syn_ack_packet.to_bytes(), sender)

        # Wait for ACK
        ack_data, _ = conn.recvfrom(1024)
        ack_packet = Packet.from_bytes(ack_data)
        if ack_packet.payload == b'ACK':
            print("Received ACK. Handshake completed.")
            return True
    return False