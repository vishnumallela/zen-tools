import logging
import os

import uvicorn
from dotenv import load_dotenv
from starlette.middleware import Middleware
from starlette.responses import Response

from zen_tools.server import mcp

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("zen_tools")

PORT = int(os.environ.get("PORT", 3000))
AUTH_SECRET = os.environ.get("AUTH_SECRET", "")


class _BearerAuth:
    def __init__(self, app) -> None:
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        path = scope.get("path", "")
        if scope["type"] == "http" and (path == "/mcp" or path.startswith("/mcp/")):
            headers = dict(scope.get("headers", []))
            if headers.get(b"authorization", b"").decode() != f"Bearer {AUTH_SECRET}":
                await Response("Unauthorized", status_code=401)(scope, receive, send)
                return
        await self.app(scope, receive, send)


app = mcp.http_app(middleware=[Middleware(_BearerAuth)] if AUTH_SECRET else None)


def main() -> None:
    log.info("zen-tools running on http://0.0.0.0:%d", PORT)
    uvicorn.run("zen_tools.main:app", host="0.0.0.0", port=PORT, log_level="info")


if __name__ == "__main__":
    main()
