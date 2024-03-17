import socket
import ssl
import threading


################## TCP #############

def tcp_query_over_tls(data, tls_server='1.1.1.1', port=853):
    context = ssl.create_default_context()

    # Establishing a TLS connection
    with socket.create_connection((tls_server, port)) as sock:
        with context.wrap_socket(sock, server_hostname=tls_server) as ssock:
            # Sending the data over TLS
            ssock.send(data)

            # Receiving the response
            response = ssock.recv(4096)
            return response

def dns_server_tcp(address='0.0.0.0', port=53):
    # Creating a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((address, port))
        server_socket.listen(5)
        print(f"DNS-over-TLS forwarding server running on {address}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            # Receiving data from the client
            data = client_socket.recv(4096)
            print(f"Received {len(data)} bytes")

            # Forwarding the query and getting the response
            response = tcp_query_over_tls(data)

            # Sending the response back to the client
            client_socket.send(response)  
            client_socket.close()
            


################## UDP #############
            
def udp_query_over_tls(data, dns_server='1.1.1.1', port=853):
    context = ssl.create_default_context()

    with socket.create_connection((dns_server, port)) as sock:
        with context.wrap_socket(sock, server_hostname=dns_server) as ssock:
            # DNS over TCP (including over TLS) requires a 2-byte length field before the DNS payload
            dns_query_with_length_prefix = len(data).to_bytes(2, byteorder='big') + data
            ssock.send(dns_query_with_length_prefix)
            
            # Read the length of the response and modify it back to be UDP compatible
            response_length_bytes = ssock.recv(2)
            response_length = int.from_bytes(response_length_bytes, byteorder='big')
            response = ssock.recv(response_length)
            
            return response

def dns_server_udp(address='0.0.0.0', port=53):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((address, port))
        print(f"DNS Proxy Server listening on {address}:{port}")
        
        while True:
            try:
                # DNS queries are typically up to 512 bytes for UDP
                data, client_address = server_socket.recvfrom(512)
                print(f"Received DNS query from {client_address}")
                
                # Forward the query over TLS and get the response
                response = udp_query_over_tls(data)
                
                # Send the response back to the client
                server_socket.sendto(response, client_address)
            except Exception as e:
                print(f"Error: {e}")

######## START ########

if __name__ == "__main__":
    tcp_thread = threading.Thread(target=dns_server_tcp)
    udp_thread = threading.Thread(target=dns_server_udp)

    tcp_thread.start()
    udp_thread.start()

    tcp_thread.join()
    udp_thread.join()