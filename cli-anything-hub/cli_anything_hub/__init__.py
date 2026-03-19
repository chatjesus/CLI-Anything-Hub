"""
cli-anything-hub — Shared auth, subscription & gating for all CLI-Anything tools.
"""

__version__ = "1.0.0"

from .auth import (
    get_credentials,
    save_credentials,
    clear_credentials,
    is_logged_in,
    is_pro,
    get_config_dir,
)
from .gate import require_pro, pro_command
