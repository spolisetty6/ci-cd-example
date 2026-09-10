"""Flask application entry point."""
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': __import__('datetime').datetime.utcnow().isoformat(),
        'version': os.getenv('APP_VERSION', '1.0.0')
    }), 200


@app.route('/ready', methods=['GET'])
def ready():
    """Readiness probe."""
    return jsonify({'ready': True}), 200


@app.route('/api/status', methods=['GET'])
def api_status():
    """API status endpoint."""
    return jsonify({
        'message': 'API is working',
        'environment': os.getenv('FLASK_ENV', 'production')
    }), 200


@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler."""
    logger.error(f'Error: {str(error)}')
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
