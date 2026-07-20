"""Minimal smoke check for local and Codex cloud environments."""

from platform import python_version


def environment_summary() -> str:
    """Return a short message confirming that Python can run the project."""
    return f"LLNL challenge environment ready (Python {python_version()})"


if __name__ == "__main__":
    print(environment_summary())
