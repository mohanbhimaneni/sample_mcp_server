
import hashlib
import os

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

# Create the MCP server
mcp = FastMCP("Exam Challenge Server")

# The email registered for this exam
EMAIL = "24f1002200@ds.study.iitm.ac.in".strip().lower()


@mcp.tool()
def solve_challenge() -> str:
    """Calculate the challenge response from the current HTTP request."""

    # Read the headers sent with this particular tool call
    headers = get_http_headers()

    # HTTP header names are case-insensitive
    challenge = headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    # Build the exact string specified in the assignment
    message = f"{challenge}:{EMAIL}"

    # Calculate SHA-256 and keep the first 16 hex characters
    digest = hashlib.sha256(message.encode("utf-8")).hexdigest()

    return digest[:16]


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8000")),
    )
