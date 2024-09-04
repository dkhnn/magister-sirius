from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    # Here you can add checks like database connectivity, etc.
    response = {
        'status': 'healthy',
        'message': 'Service is up and running'
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)