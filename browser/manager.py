from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from utils.logger import log
from config import CDP_URL, PRODUCT_URL


class BrowserManager:

    def __init__(self, playwright):

        self.playwright = playwright
        self.browser = None
        self.context = None

    async def connect(self):

        log("Connecting to existing Chrome...")

        try:

            self.browser = (
                await self.playwright.chromium.connect_over_cdp(
                    CDP_URL
                )
            )

        except Exception as e:

            log("Cannot connect to Chrome.")

            log(
                "Please start Chrome with "
                "--remote-debugging-port=9222"
            )

            raise e

        if not self.browser.contexts:

            raise RuntimeError(
                "No browser context found."
            )

        self.context = self.browser.contexts[0]

        log("Connected to Chrome successfully.")

        return self.context

    async def find_product_page(self):

        for page in self.context.pages:

            try:

                if PRODUCT_URL in page.url:

                    log(
                        "Found existing product page."
                    )

                    return page

            except Exception:

                continue

        return None

    async def open_product_page(self):

        page = await self.find_product_page()

        if page:

            return page

        log("Product page not found.")

        log("Opening product page...")

        page = await self.context.new_page()

        await page.goto(
            PRODUCT_URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        return page

    async def prepare_page(self, page):

        try:

            await page.bring_to_front()

        except Exception:

            pass

        try:

            await page.wait_for_load_state(
                "domcontentloaded",
                timeout=30000
            )

        except PlaywrightTimeoutError:

            pass

        await page.wait_for_timeout(3000)

        log(
            f"Page title: {await page.title()}"
        )

        log(
            f"Current URL: {page.url}"
        )