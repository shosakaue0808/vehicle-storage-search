from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/store-vehicles', methods=['POST'])
def store_vehicles():
    data = request.json
    # Process your input data here (vehicle length, quantity)
    
    response = {
        "message": "Data received successfully",
        "data": data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)