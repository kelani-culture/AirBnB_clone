#!/usr/bin/env python3
"""package initializer for the models directory"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
