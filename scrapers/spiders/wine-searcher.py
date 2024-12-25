import scrapy
from scrapy import Request
import logging
from playwright_stealth import stealth_async
import random
import asyncio

ALLOWED_ERROR_STATUS_CODES = [403, 557]


async def mimic_human_interaction(page):
    """Simulate human-like interactions to avoid detection."""
    # Random mouse movements
    await page.mouse.move(random.randint(0, 1000), random.randint(0, 800))
    await asyncio.sleep(random.uniform(1, 3))

    # Random key presses
    await page.keyboard.press("ArrowDown")
    await asyncio.sleep(random.uniform(1, 2))

    # Random scrolling
    await page.evaluate("window.scrollBy(0, window.innerHeight)")
    await asyncio.sleep(random.uniform(1, 3))

    # Random mouse clicks
    await page.mouse.click(random.randint(50, 300), random.randint(50, 300))
    await asyncio.sleep(random.uniform(2, 5))


class WineSpider(scrapy.Spider):
    name = "wine_searcher"
    # allowed_domains = ["wine-searcher.com"]
    start_urls = [
        # "https://www.wine-searcher.com/find/de+pibarnon+bandol+provence+france",
        # "https://arh.antoinevastel.com/bots/areyouheadless",
        "https://arh.antoinevastel.com/bots/"
    ]

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://www.google.com/",
            "Alt-Used": "www.wine-searcher.com",
            "Connection": "keep-alive",
            "Cookie": "cookie_enabled=true; ID=34GHC790KV700TM; IDPWD=I34265814; user_status=A%7C; find_tab=%23t2; _csrf=xNCuawrUWoLESE6S4AOugSbehWjzo0A7; cookie_enabled=true; COOKIE_ID=34GHC790KV700TM; visit=34GHC790KV700TM%7C20241116232742%7C%2Ffind%2Fchateau%2Bde%2Bpibarnon%7C%7Cend%20; fflag=flag_ab_testing%3A0%2Cend; search=start%7Cde%2Bpibarnon%2Bbandol%2Bprovence%2Bfrance%7C1%7Cany%7CUSD%7C%7C%7C%7C%7C%7C%7C%7C%7Ce%7Ci%7C%7C%7CN%7C%7Ca%7C%7C%7C%7CCUR%7Cend; cookie_consent=0; _pxhd=pQ0i1qD3gO9RlCm-Qfbk7ex53Eb3wBtcFzsAfwEQoicUg7jdRsH-mEzrSH1SG7Rvt3A5TF4vo8yBqZp5hv1gcg==:sHzVQ4MKlWwCoLBqXoH01OZPTwFpn99jsm2wsZPanNGM8M0LynkKYWc7EXs58V2PxoOETXiNLqkuuEdJNczRPSHDlWL1KlwxQLExHfQPRMw=; mrkloc=Czech%2BRepublic%7CCZ%7C%7CCzech%2BRepublic-CZ-%3B%20path%3D%2F%3B%20domain%3Dwine-searcher.com%3B%20expires%3DTue%2C%2031-Dec-2030%2000%3A00%3A00%20GMT; cookie_enabled=true; adin=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzE5MjM3MDguODI0MzQ5LCJleHAiOjE3NzIwOTk3MDguODI0MzQ5LCJ1aWQiOm51bGwsInVlYSI6bnVsbCwidWFjZCI6bnVsbH0.Ozs-xuG_qYmrrEqtMHPIX0xpJ2ZRrPPMnvsuchzLw44; fflag=flag_ab_testing%3A0%2Cend; search=start%7Cde%2Bpibarnon%2Bbandol%2Bprovence%2Bfrance%7C1%7Cany%7CUSD%7C%7C%7C%7C%7C%7C%7C%7C%7Ce%7Ci%7C%7C%7CN%7C%7Ca%7C%7C%7C%7CCUR%7Cend; COOKIE_ID=D2PHC36FKQ100SM; ID=D2PHC36FKQ100SM; IDPWD=I74562238; _csrf=VUcPL0eeV-P9V5MSdJLFvPxdDf1gfFB4; _pxhd=PpOEZ9k9lVIoAQtQc1xu9lCkOsQpB8LPL24rZmrzkMjaXUi3Ro-2rNEdJ3Zh5/bqFnrjfu2W60irbOhncxehhQ==:Z6jiUSjviSc9Lr0keW5-T2ZopQ/q2izzrgrT2QKtf/ChP1OTnFVZc-xgDWJCSdiYAbVLcEZM7kinlDt1kg3SYgKmeG5-pOArFMhrKNSefyw=; cookie_consent=0; find_tab=%23t1; user_status=A%7C",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "DNT": "1",
            "Sec-GPC": "1",
            "Priority": "u=0, i",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
            "scrapers.middlewares.retry.RetryMiddleware": 550,
        },
        # Set up Scrapoxy settings and credentials
        # Replace the default Scrapy downloader with Playwright and Chrome to manage JavaScript content.
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        # Set up Playwright to launch the browser in headful mode using Scrapoxy.
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
            "proxy": {
                "server": "http://mp.evomi.com:3000",
                "username": "matthewabe",
                "password": "WDF1Y7Fx1sukqXndrX0r",
            },
            "args": [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
            ],
        },
    }

    def start_requests(self):
        """Initiate a request using Playwright."""
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                meta=dict(
                    handle_httpstatus_list=ALLOWED_ERROR_STATUS_CODES,
                    # Enable Playwright
                    playwright=True,
                    # Include the Playwright page object in the response
                    playwright_include_page=True,
                    playwright_context="context",
                    playwright_context_kwargs=dict(
                        # Ignore HTTPS errors
                        ignore_https_errors=True,
                        timezone_id="Europe/Berlin",
                    ),
                    playwright_page_goto_kwargs=dict(
                        wait_until="networkidle",
                    ),
                ),
            )

    async def parse(self, response):
        """Parse the page content after clicking the button and taking a screenshot."""
        page = response.meta["playwright_page"]

        # Apply stealth to the Playwright page to disguise automation
        await stealth_async(page)

        # Disable navigator.webdriver property to avoid detection
        await page.evaluate("delete navigator.webdriver")

        try:
            # Take a screenshot after clicking the button
            await page.screenshot(path="screenshot.png", full_page=True)
            logging.info("Screenshot taken.")
            # if response.status in ALLOWED_ERROR_STATUS_CODES:
            #     logging.warning("Received 403 Forbidden. Saving the HTML content.")

            #     # Save the HTML content to a file for debugging
            #     html_content = await page.content()
            #     with open("403_response.html", "w", encoding="utf-8") as f:
            #         f.write(html_content)
            #     logging.info("Saved 403 response to 403_response.html")

            # # Wait for the page to load
            # await page.wait_for_selector("body")
            # logging.info("Page loaded successfully.")

            # # Mimic human interaction to avoid detection
            # await mimic_human_interaction(page)

            # # Add a random delay before proceeding
            # await asyncio.sleep(random.uniform(3, 6))

            # # Click the button to reveal more info
            # await page.click("#find-tab-info")
            # logging.info("Clicked on the button.")

            # # Wait for the info section to load
            # await page.wait_for_selector("#info-card")
            # logging.info("Info section loaded.")

            # # Take a screenshot after clicking the button
            # await page.screenshot(path="screenshot.png", full_page=True)
            # logging.info("Screenshot taken.")

            # # Extract wine details using a CSS selector
            # wine_name = await page.evaluate(
            #     'document.querySelector("#tab-info")?.innerText'
            # )
            # logging.info(f"Extracted wine name: {wine_name}")

            # yield {"data": wine_name}

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        finally:
            await page.close()
