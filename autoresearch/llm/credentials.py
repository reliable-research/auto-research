"""Credential mapper and environment detector for Antigravity (agy) & Gemini."""

import os
import shutil
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AgyAuthStatus:
    is_valid: bool
    agy_binary: Optional[str] = None
    agy_version: Optional[str] = None
    token_path: Optional[str] = None
    auth_method: Optional[str] = None
    token_preview: Optional[str] = None
    error_message: Optional[str] = None


class AgyCredentialMapper:
    """Discovers, maps, and validates credentials from Antigravity CLI."""

    def __init__(
        self,
        token_path: Optional[str] = None,
        agy_binary: Optional[str] = None,
    ):
        self.token_path = Path(
            token_path
            or os.environ.get("AGY_TOKEN_PATH")
            or os.path.expanduser("~/.gemini/antigravity-cli/antigravity-oauth-token")
        )
        self.agy_binary = agy_binary or self._find_agy_binary()

    def _find_agy_binary(self) -> Optional[str]:
        """Find the agy executable in standard locations or PATH."""
        env_path = os.environ.get("AGY_PATH")
        if env_path and os.path.isfile(env_path) and os.access(env_path, os.X_OK):
            return env_path

        local_bin = os.path.expanduser("~/.local/bin/agy")
        if os.path.isfile(local_bin) and os.access(local_bin, os.X_OK):
            return local_bin

        system_which = shutil.which("agy")
        if system_which:
            return system_which

        return None

    def get_token_data(self) -> Dict[str, Any]:
        """Read and parse the local oauth token file."""
        if not self.token_path.exists():
            raise FileNotFoundError(f"OAuth token not found at {self.token_path}")
        try:
            with open(self.token_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to read/parse token from {self.token_path}: {e}")

    def get_bearer_token(self) -> Optional[str]:
        """Extract the bearer access token string."""
        try:
            data = self.get_token_data()
            token_obj = data.get("token")
            if isinstance(token_obj, dict):
                return token_obj.get("access_token")
            elif isinstance(token_obj, str):
                return token_obj
            return None
        except Exception:
            return None

    def get_token_details(self) -> Dict[str, Any]:
        """Return structured token details (expiry, token_type, auth_method)."""
        try:
            data = self.get_token_data()
            token_obj = data.get("token", {})
            if isinstance(token_obj, dict):
                return {
                    "access_token": token_obj.get("access_token"),
                    "token_type": token_obj.get("token_type", "Bearer"),
                    "expiry": token_obj.get("expiry"),
                    "has_refresh_token": bool(token_obj.get("refresh_token")),
                    "auth_method": data.get("auth_method", "oauth"),
                }
            elif isinstance(token_obj, str):
                return {
                    "access_token": token_obj,
                    "token_type": "Bearer",
                    "auth_method": data.get("auth_method", "oauth"),
                }
        except Exception as e:
            return {"error": str(e)}
        return {}

    def get_auth_headers(self) -> Dict[str, str]:
        """Generate Authorization header dictionary."""
        token = self.get_bearer_token()
        if not token:
            raise RuntimeError("Cannot construct auth headers: No bearer token found.")
        return {"Authorization": f"Bearer {token}"}

    def map_to_env(self) -> Dict[str, str]:
        """Export credentials to standard environment variables for subprocesses."""
        token = self.get_bearer_token()
        exported = {}
        if token:
            os.environ["ANTIGRAVITY_OAUTH_TOKEN"] = token
            os.environ["GOOGLE_OAUTH_ACCESS_TOKEN"] = token
            exported["ANTIGRAVITY_OAUTH_TOKEN"] = f"{token[:8]}...{token[-4:]}"
        if self.agy_binary:
            os.environ["AGY_PATH"] = self.agy_binary
            exported["AGY_PATH"] = self.agy_binary
        return exported

    def check_status(self) -> AgyAuthStatus:
        """Perform a non-intrusive status check of the agy installation and token."""
        binary = self._find_agy_binary()
        if not binary:
            return AgyAuthStatus(
                is_valid=False,
                error_message="`agy` binary not found in ~/.local/bin or PATH.",
            )

        # Get agy version if possible
        version_str = None
        try:
            res = subprocess.run([binary, "--help"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                version_str = "Antigravity CLI (agy)"
        except Exception:
            pass

        if not self.token_path.exists():
            return AgyAuthStatus(
                is_valid=False,
                agy_binary=binary,
                agy_version=version_str,
                error_message=f"Antigravity token file not found at {self.token_path}",
            )

        try:
            token = self.get_bearer_token()
            data = self.get_token_data()
            auth_method = data.get("auth_method", "oauth")
            if not token:
                return AgyAuthStatus(
                    is_valid=False,
                    agy_binary=binary,
                    token_path=str(self.token_path),
                    error_message="Token file missing valid access_token.",
                )

            preview = f"{token[:8]}...{token[-4:]}"
            return AgyAuthStatus(
                is_valid=True,
                agy_binary=binary,
                agy_version=version_str,
                token_path=str(self.token_path),
                auth_method=auth_method,
                token_preview=preview,
            )
        except Exception as e:
            return AgyAuthStatus(
                is_valid=False,
                agy_binary=binary,
                token_path=str(self.token_path),
                error_message=str(e),
            )
