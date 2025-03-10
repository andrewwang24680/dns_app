from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

@app.route("/register", methods=["PUT"])
def register():
    data = request.json
    if not all(k in data for k in ["hostname", "ip", "as_ip", "as_port"]):
        return "Bad Request - Missing Parameters", 400

    message = f"TYPE=A\nNAME={data['hostname']}\nVALUE={data['ip']}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (data["as_ip"], int(data["as_port"])))
    sock.close()

    return "Registered Successfully", 201

def fibonacci(n):
    if n == 0: return 0
    elif n == 1: return 1
    else:
        a, b = 0, 1
        for _ in range(2, n+1):
            a, b = b, a + b
        return b

@app.route("/fibonacci", methods=["GET"])
def get_fibonacci():
    number = request.args.get("number")
    if not number.isdigit():
        return "Bad Request - Invalid Number", 400
    
    return jsonify({"Fibonacci": fibonacci(int(number))}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9090)
