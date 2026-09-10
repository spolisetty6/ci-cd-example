import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
port = os.getenv('PORT', 5000)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'python-api'
    }), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Ready probe endpoint"""
    return jsonify({'ready': True}), 200

@app.route('/api/status', methods=['GET'])
def api_status():
    """API status endpoint"""
    return jsonify({
        'message': 'API is working',
        'environment': os.getenv('FLASK_ENV', 'production')
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port), debug=os.getenv('FLASK_ENV') == 'development')
