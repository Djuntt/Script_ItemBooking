import asyncio

from playwright.async_api import async_playwright

from config import (
    CHECK_INTERVAL,
    AUTO_ADD_TO_BAG,
    AUTO_BUY_NOW
)

from browser.manager import BrowserManager
from monitor.stock import StockMonitor
from purchase.actions import PurchaseActions
from utils.logger import log


async def monitor(page):

    stock_monitor = StockMonitor(page)

    purchase = PurchaseActions(page)

    attempt = 0

    log("")
    log("==============================")
    log(" POP MART STOCK BOT")
    log("==============================")
    log("")

    while True:

        attempt += 1

        log(
            f"Checking stock... "
            f"(attempt {attempt})"
        )

        try:

            # Refresh page
            await page.reload(
                wait_until="domcontentloaded",
                timeout=30000
            )

            # Allow JavaScript to render
            await page.wait_for_timeout(1500)

            # Check stock
            status = (
                await stock_monitor.check_stock()
            )

            # --------------------------------
            # SOLD OUT
            # --------------------------------

            if status is False:

                log(
                    "Status: SOLD OUT"
                )

            # --------------------------------
            # AVAILABLE
            # --------------------------------

            elif status is True:

                log(
                    "🔥 PRODUCT MAY BE AVAILABLE!"
                )

                # ----------------------------
                # Add to Bag
                # ----------------------------

                if AUTO_ADD_TO_BAG:

                    success = (
                        await purchase.add_to_bag()
                    )

                    if success:

                        log("")
                        log(
                            "=============================="
                        )
                        log(
                            " PRODUCT ADDED TO BAG"
                        )
                        log(
                            "=============================="
                        )

                        log(
                            "Automation stopped."
                        )

                        return

                # ----------------------------
                # Buy Now
                # ----------------------------

                if AUTO_BUY_NOW:

                    success = (
                        await purchase.buy_now()
                    )

                    if success:

                        log("")
                        log(
                            "=============================="
                        )
                        log(
                            " BUY NOW CLICKED"
                        )
                        log(
                            "=============================="
                        )

                        log(
                            "Automation stopped."
                        )

                        return

            # --------------------------------
            # UNKNOWN
            # --------------------------------

            else:

                log(
                    "Status: UNKNOWN"
                )

                # Every 10 attempts inspect UI
                if attempt % 10 == 0:

                    await stock_monitor.inspect_buttons()

        except Exception as e:

            log(
                f"Monitoring error: {e}"
            )

        await asyncio.sleep(
            CHECK_INTERVAL
        )


async def main():

    async with async_playwright() as playwright:

        browser_manager = (
            BrowserManager(playwright)
        )

        # Connect Chrome
        context = (
            await browser_manager.connect()
        )

        # Find or open product page
        page = (
            await browser_manager.open_product_page()
        )

        # Prepare page
        await browser_manager.prepare_page(
            page
        )

        # Start monitoring
        await monitor(page)


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        log("Bot stopped by user.")