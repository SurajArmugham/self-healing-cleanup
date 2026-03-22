# app/routes.py

from flask import Blueprint, request, jsonify
from app.service import run_cleanup_service

bp = Blueprint("routes", __name__)


@bp.route("/cleanup", methods=["POST"])
def cleanup():
    """
    API endpoint triggered by ServiceNow
    """

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