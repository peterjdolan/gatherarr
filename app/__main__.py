"""Entry point for running as module."""

import asyncio

from app.main import main

if __name__ == "__main__":
  asyncio.run(main())
