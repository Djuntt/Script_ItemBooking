from config import TIMEOUT
from utils.logger import log


class PurchaseActions:

    def __init__(self, page):
        self.page = page

    async def find_button(self, button_names):
        for name in button_names:
            try:
                locator = self.page.get_by_role(
                    "button",
                    name=name,
                    exact=True
                )

                count = await locator.count()

                for i in range(count):
                    button = locator.nth(i)

                    if await button.is_visible():
                        return button

            except Exception:
                pass

        return None

    async def buy_now(self):
        log("Searching for Buy Now button...")

        button = await self.find_button(
            [
                "BUY NOW",
                "Buy Now",
                "立即购买"
            ]
        )

        if button is None:
            log("Buy Now button not found.")
            return False

        try:
            await button.scroll_into_view_if_needed()

            # 记录当前页面数量
            context = self.page.context
            old_pages = len(context.pages)

            await button.click(timeout=TIMEOUT)

            log("Successfully clicked Buy Now.")

            # 等待页面变化
            await self.page.wait_for_timeout(2000)

            # 如果打开了新页面，使用新页面
            if len(context.pages) > old_pages:
                new_page = context.pages[-1]

                await new_page.wait_for_load_state(
                    "domcontentloaded",
                    timeout=TIMEOUT
                )

                log("New page opened.")
            else:
                # 如果是在当前页面跳转
                new_page = self.page

                log("Checkout opened in the current page.")

            log(f"Checkout URL: {new_page.url}")

            # 查找 CHECK NOW
            log("Searching for CHECK NOW button...")

            check_button = await self.find_check_button(new_page)

            if check_button is None:
                log("CHECK NOW button not found.")
                return False

            await check_button.scroll_into_view_if_needed()
            await check_button.click(timeout=TIMEOUT)

            log("Successfully clicked CHECK NOW.")

            return True

        except Exception as e:
            log(f"Buy Now / Check Now failed: {e}")
            return False

    async def find_check_button(self, page):
        for name in [
            "CHECK NOW",
            "Check Now",
            "PROCEED TO PAY"
        ]:
            try:
                locator = page.get_by_role(
                    "button",
                    name=name,
                    exact=True
                )

                count = await locator.count()

                for i in range(count):
                    button = locator.nth(i)

                    if await button.is_visible() and not await button.is_disabled():
                        return button

            except Exception:
                pass

        return None