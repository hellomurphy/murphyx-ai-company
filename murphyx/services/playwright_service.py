"""
Playwright service — browser automation facade.

No hardcoded targets or marketplace URLs — inject via task payload only.
Optional dependency: install `playwright` when browser automation is needed.
"""

from __future__ import annotations

from murphyx.observability import get_logger

logger = get_logger("playwright")


async def run_script(url: str, steps: list[dict]) -> dict:
    """Execute browser automation steps. Requires `playwright` to be installed."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return {"error": "playwright not installed — pip install playwright"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        results: list[str] = []
        for step in steps:
            action = step.get("action", "")
            selector = step.get("selector", "")
            if action == "click" and selector:
                await page.click(selector)
                results.append(f"clicked {selector}")
            elif action == "fill" and selector:
                await page.fill(selector, step.get("value", ""))
                results.append(f"filled {selector}")
            elif action == "screenshot":
                path = step.get("path", "screenshot.png")
                await page.screenshot(path=path)
                results.append(f"screenshot saved to {path}")
        await browser.close()
    return {"url": url, "steps_executed": len(results), "log": results}
