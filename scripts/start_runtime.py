#!/usr/bin/env python3
"""Dev entry — start the MurphyX worker loop."""

import asyncio

from murphyx.runtime.worker_loop import run_worker_loop

if __name__ == "__main__":
    asyncio.run(run_worker_loop())
