"""Entry point for desktop AND web (pygbag).

pygbag looks for a top-level ``main.py`` and an ``asyncio.run(main())`` call, so
this file is the single source of truth for launching the game on both targets.
"""
import asyncio
from zdg.app import main

if __name__ == "__main__":
    asyncio.run(main())
