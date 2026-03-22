import os
import app.config as config
from app.cleanup.utils import get_file_age_in_days, is_file
from app.logger import setup_logger

logger = setup_logger()


def cleanup_old_files():
    deleted_files = 0
    errors = 0

    logger.info(f"Starting cleanup in directory: {config.CLEANUP_DIRECTORY}")

    if not os.path.exists(config.CLEANUP_DIRECTORY):
        logger.error(f"Directory does not exist: {config.CLEANUP_DIRECTORY}")
        return {
            "status": "failed",
            "reason": "Directory not found"
        }

    for filename in os.listdir(config.CLEANUP_DIRECTORY):
        file_path = os.path.join(config.CLEANUP_DIRECTORY, filename)

        try:
            if is_file(file_path):
                age = get_file_age_in_days(file_path)

                if age > config.RETENTION_DAYS:
                    os.remove(file_path)
                    deleted_files += 1

                    logger.info(f"Deleted file: {file_path} (age: {age} days)")

        except Exception as e:
            errors += 1
            logger.error(f"Error deleting {file_path}: {str(e)}")

    logger.info(f"Cleanup completed. Deleted: {deleted_files}, Errors: {errors}")

    return {
        "status": "success",
        "deleted_files": deleted_files,
        "errors": errors
    }