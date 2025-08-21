# config.py
# Database credentials and application settings

import os
from typing import Dict, Any

# Database configuration
DB_CONFIG: Dict[str, Any] = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "admin123"),
    "database": os.getenv("DB_NAME", "library_management_system"),
    "autocommit": True,
    "charset": "utf8mb4"
}

# Application settings
APP_CONFIG: Dict[str, Any] = {
    "fine_rate_per_day": 5.0,  # Fine amount per day in currency
    "grace_period_days": 14,   # Days before fine starts
    "max_books_per_member": 5, # Maximum books a member can borrow
    "default_return_period": 30 # Default return period in days
}

# Logging configuration
LOG_CONFIG: Dict[str, Any] = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "library_system.log"
}
