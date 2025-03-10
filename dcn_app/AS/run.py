import socket
import json

DNS_DB_FILE = "dns_records.json"

def load_dns_records():
    try:
        with open(DNS_DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_dns_records(records):
    with open(DNS_DB_FILE, "w") as f:
        json.dump(records, f)

def handle_registration(data):
    records = load_dns_records()
    hostname = data["NAME"]
    records[hostname] = {"VALUE": data["VALUE"], "TTL": data["TTL"]}
    save_dns_records(records)
    return "Registration Successful"

def handle_query(data):
    records = load_dns_records()
    hostname = data["NAME"]
    if hostname in records:
        return f"TYPE=A\nNAME={hostname}\nVALUE={records[hostname]['VALUE']}\nTTL={records[hostname]['TTL']}\n"
    return "Host Not Found"

def parse_message(msg):
    lines = msg.decode().split("\n")
    data = {line.split("=")[0]: line.split("=")[1] for line in lines if "=" in line}
    return data

def start_dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 53533))

    while True:
        message, client_addr = sock.recvfrom(1024)
        data = parse_message(message)

        if "VALUE" in data:
            response = handle_registration(data)
        else:
            response = handle_query(data)

        sock.sendto(response.encode(), client_addr)

if __name__ == "__main__":
    start_dns_server()
