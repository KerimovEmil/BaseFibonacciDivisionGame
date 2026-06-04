"""Backwards-compatible desktop launcher. Prefer `python main.py`."""
import asyncio
from zdg.app import main

if __name__ == '__main__':
    asyncio.run(main())
