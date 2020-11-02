#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and "
                          "available on your PYTHONPATH environment variable? Did you "
                          "forget to activate a virtual environment?") from exc

    # This allows easy placement of apps within the interior r-sgwfc-gene-web
    # directory.
    root_path = Path(__file__).resolve().parent
    sys.path.append(root_path / 'r-sgwfc-gene-web')

    execute_from_command_line(sys.argv)
