"""
Package shim to make `src/ecommerce` an importable package while keeping the
existing codebase layout. This shim adds the repository root to sys.path so
imports continue to resolve without changing runtime code.

This file is intentionally minimal and non-invasive. It's a temporary helper
until we perform a proper git-backed move (preserves history) across the repo.
"""
import os
import sys

# Ensure repo root is on sys.path so existing top-level modules are importable
_this_dir = os.path.dirname(__file__)
_repo_root = os.path.abspath(os.path.join(_this_dir, '..', '..'))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

__all__ = []
