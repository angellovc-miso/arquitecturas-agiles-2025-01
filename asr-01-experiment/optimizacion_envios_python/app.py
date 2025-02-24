from flask import Flask, jsonify
import time
import os

app = Flask(__name__)
request_count = 0


@app.route('/optimizacion_envios', methods=['GET'])
def get_envios():
    global request_count
    request_count = request_count + 1

    if request_count % 30 == 0:
        time.sleep(10)

    return jsonify(
        {
          "altitude": 15.2,
          "latitude": 37.7749,
          "longitude": -122.4194,
          "coordinate_system": "Python - Delivery optimization service",
        }
    )

if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))
    app.run(debug=True, host='0.0.0.0', port=port)
