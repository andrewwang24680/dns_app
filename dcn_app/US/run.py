from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

def query_dns(hostname, as_ip, as_port):
    """ Queries the authoritative server for the IP address of the given hostname """
    message = f"TYPE=A\nNAME={hostname}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, int(as_port)))
    
    response, _ = sock.recvfrom(1024)
    sock.close()
    
    lines = response.decode().split("\n")
    for line in lines:
        if line.startswith("VALUE="):
            return line.split("=")[1]
    return None

@app.route("/fibonacci", methods=["GET"])
def get_fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request - Missing Parameters", 400

    fs_ip = query_dns(hostname, as_ip, as_port)
    if not fs_ip:
        return "DNS resolution failed", 404

    response = requests.get(f"http://{fs_ip}:{fs_port}/fibonacci?number={number}")
    return response.text, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
