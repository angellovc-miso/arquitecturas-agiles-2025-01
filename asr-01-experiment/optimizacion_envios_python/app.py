from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/optimizacion_envios', methods=['GET'])
def get_envios():
    return jsonify(
        {
          "altitude": 15.2,
          "latitude": 37.7749,
          "longitude": -122.4194,
          "coordinate_system": "Python - Delivery optimization service",
        }
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
