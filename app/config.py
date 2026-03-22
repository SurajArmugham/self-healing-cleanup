# app/config.py

import os

# Base directory for cleanup (SAFE test directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory to clean (change later if needed)
CLEANUP_DIRECTORY = os.path.join("/tmp", "test_cleanup")

# Retention policy (days)
RETENTION_DAYS = 7

# Log file path
LOG_FILE = os.path.join(BASE_DIR, "logs", "cleanup.log")