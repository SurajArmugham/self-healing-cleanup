# app/routes.py

from flask import Blueprint, request, jsonify
from app.service import run_cleanup_service
import app.config as config

bp = Blueprint("routes", __name__)


@bp.route("/cleanup", methods=["POST"])
def cleanup():
    """
    API endpoint triggered by ServiceNow
    """
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key != config.API_KEY:
        return jsonify({
            "status": "unauthorized",
            "message": "Invalid API Key"
        }), 401
    
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": "failed",
                "reason": "Invalid JSON input"
            }), 400

        result = run_cleanup_service(data)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        }), 500