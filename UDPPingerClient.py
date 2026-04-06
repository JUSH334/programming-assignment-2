# UDPPingerClient.py
import time
from socket import *

# Server address and port
serverName = '127.0.0.1'
serverPort = 12000

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Set socket timeout to 1 second
clientSocket.settimeout(1)

# Track RTTs for statistics
rtts = []

# Send 10 pings
for sequence_number in range(1, 11):
    # Record the send time
    sendTime = time.perf_counter()

    # Create the ping message
    message = f"Ping {sequence_number} {sendTime}"

    try:
        # Send the ping message to the server
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # Receive the server's response
        response, serverAddress = clientSocket.recvfrom(1024)

        # Record the receive time and calculate RTT
        receiveTime = time.perf_counter()
        rtt = receiveTime - sendTime
        rtts.append(rtt)

        # Print the response and RTT
        print(f"Reply from {serverName}: {response.decode()}  RTT = {rtt:.6f} seconds")

    except timeout:
        print("Request timed out")

# Print statistics
print("\n--- Ping statistics ---")
print(f"Packets: Sent = 10, Received = {len(rtts)}, Lost = {10 - len(rtts)} ({(10 - len(rtts)) * 10}% loss)")
if rtts:
    print(f"Minimum RTT = {min(rtts):.6f} seconds")
    print(f"Maximum RTT = {max(rtts):.6f} seconds")
    print(f"Average RTT = {(sum(rtts) / len(rtts)):.6f} seconds")

# Close the socket
clientSocket.close()
