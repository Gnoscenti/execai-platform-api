"""
Main Flask application for the EXECAI Platform API.

This module initializes the Flask application and defines the API endpoints
for the EXECAI Platform, including knowledge retrieval and Strategic Catalyst
persona interactions.
"""

import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Add the parent directory to sys.path to allow imports from the project root
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Import knowledge base and persona modules
from knowledge.enhanced_knowledge_base import EnhancedKnowledgeBase
from personas.strategic_catalyst import StrategicCatalyst

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize knowledge base and personas
knowledge_base = EnhancedKnowledgeBase()
strategic_catalyst = StrategicCatalyst(knowledge_base)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/knowledge/domains', methods=['GET'])
def get_knowledge_domains():
    """Get all available knowledge domains."""
    domains = knowledge_base.get_domains()
    return jsonify({
        'domains': domains,
        'count': len(domains)
    })

@app.route('/api/knowledge/query', methods=['POST'])
def query_knowledge():
    """Query the knowledge base with specific parameters."""
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({
            'error': 'Missing required parameter: query'
        }), 400
    
    query = data['query']
    domains = data.get('domains', [])
    capabilities = data.get('capabilities', [])
    
    results = knowledge_base.query(
        query=query,
        domains=domains,
        capabilities=capabilities
    )
    
    return jsonify(results)

@app.route('/api/personas/strategic-catalyst/respond', methods=['POST'])
def strategic_catalyst_respond():
    """Get a response from the Strategic Catalyst persona."""
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({
            'error': 'Missing required parameter: query'
        }), 400
    
    query = data['query']
    context = data.get('context', [])
    
    response = strategic_catalyst.respond(
        query=query,
        context=context
    )
    
    return jsonify(response)

@app.route('/api/personas/strategic-catalyst/profile', methods=['GET'])
def strategic_catalyst_profile():
    """Get the Strategic Catalyst persona profile."""
    profile = strategic_catalyst.get_profile()
    return jsonify(profile)

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
