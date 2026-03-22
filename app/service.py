# app/service.py

from datetime import datetime
from app.cleanup.file_cleanup import cleanup_old_files
from app.logger import setup_logger

logger = setup_logger()


def run_cleanup_service(request_data):
    """
    Orchestrates cleanup process with incident context
    """

    incident_id = request_data.get("incident", "UNKNOWN")
    server = request_data.get("server", "UNKNOWN")

    logger.info(f"Cleanup triggered for Incident: {incident_id}, Server: {server}")

    start_time = datetime.now()

    try:
        cleanup_result = cleanup_old_files()

        end_time = datetime.now()

        response = {
            "incident": incident_id,
            "server": server,
            "status": cleanup_result.get("status"),
            "deleted_files": cleanup_result.get("deleted_files", 0),
            "errors": cleanup_result.get("errors", 0),
            "start_time": str(start_time),
            "end_time": str(end_time)
        }

        logger.info(f"Cleanup completed for Incident: {incident_id} → {response}")

        return response

    except Exception as e:
        logger.error(f"Cleanup failed for Incident: {incident_id} → {str(e)}")

        return {
            "incident": incident_id,
            "server": server,
            "status": "failed",
            "error": str(e)
        }