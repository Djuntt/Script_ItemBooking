
from config import TIMEOUT
from utils.logger import log


class StockMonitor:

    def __init__(self, page):
        self.page = page

    async def check_stock(self):
        """
        Check whether the current product has an active
        BUY NOW button.

        Returns:
            True  -> BUY NOW is available
            False -> BUY NOW is not available
        """

        try:

            # Find the BUY NOW button on the current page.
            button = self.page.get_by_role(
                "button",
                name="BUY NOW",
                exact=True
            )

            count = await button.count()

            if count == 0:
                return False

            # Check all matching buttons.
            for i in range(count):

                current_button = button.nth(i)

                if not await current_button.is_visible():
                    continue

                # If the button is disabled, it is not available.
                if await current_button.is_disabled():
                    continue

                log("🔥 BUY NOW detected!")

                return True

            return False

        except Exception as e:

            log(f"Stock check error: {e}")

            return False
