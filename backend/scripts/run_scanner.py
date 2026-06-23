import asyncio
from app.ble.scanner import BleScannerService
from app.core.logging import configure_logging
from app.db.init_db import init_db


async def main() -> None:
    configure_logging()
    await init_db()
    scanner = BleScannerService()
    await scanner.run_forever()


if __name__ == "__main__":
    asyncio.run(main())
