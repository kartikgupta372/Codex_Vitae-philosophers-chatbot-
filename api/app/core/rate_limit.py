"""
Basic in-memory rate limiter for /chat -- caps requests per IP per time
window. This exists specifically because deploying a publicly reachable LLM
endpoint with real per-call API cost, and zero protection against a scripted
loop hitting it repeatedly, is a genuine and avoidable financial exposure --
not a hypothetical one.

Deliberately simple: no Redis dependency (though Redis is already provisioned
in docker-compose for exactly this, unused so far), no external rate-limit
library, no new pip install. In-memory means the count resets on restart and
does NOT share state across multiple server processes/instances -- correct
and sufficient for a single-instance deploy, and a real limitation the moment
this scales beyond one process. Upgrade to a Redis-backed limiter (the infra
already exists) before that happens, not after.
"""
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

_WINDOW_SECONDS = 60
_MAX_REQUESTS_PER_WINDOW = 10  # ~10 messages/minute/IP: generous for a real
# back-and-forth conversation, restrictive enough to blunt a scripted loop.

_request_log: dict[str, deque] = defaultdict(deque)


def check_rate_limit(request: Request) -> None:
    """FastAPI dependency -- raise 429 if this IP has exceeded the window,
    otherwise record this request and let it through."""
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    log = _request_log[ip]

    while log and log[0] < now - _WINDOW_SECONDS:
        log.popleft()

    if len(log) >= _MAX_REQUESTS_PER_WINDOW:
        raise HTTPException(
            status_code=429,
            detail="Too many messages -- please wait a moment before sending another.",
        )

    log.append(now)
