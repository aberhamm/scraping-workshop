from typing import Dict
import scrapy
from scrapy import Request
import logging
from playwright_stealth import stealth_async
import random
import asyncio
from scrapy.http.headers import Headers
import playwright

ALLOWED_ERROR_STATUS_CODES = [403, 557]
REQUEST_HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "connection": "close",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    # "Accept-Language": "en-GB,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br, zstd",
    # "Referer": "https://www.google.com/",
    # "Connection": "keep-alive",
    # "Cookie": "cookie_enabled=true; ID=34GHC790KV700TM; IDPWD=I34265814; user_status=A%7C; find_tab=%23t2; _csrf=xNCuawrUWoLESE6S4AOugSbehWjzo0A7; cookie_enabled=true; COOKIE_ID=34GHC790KV700TM; visit=34GHC790KV700TM%7C20241116232742%7C%2Ffind%2Fchateau%2Bde%2Bpibarnon%7C%7Cend%20; fflag=flag_ab_testing%3A0%2Cend; search=start%7Cde%2Bpibarnon%2Bbandol%2Bprovence%2Bfrance%7C1%7Cany%7CUSD%7C%7C%7C%7C%7C%7C%7C%7C%7Ce%7Ci%7C%7C%7CN%7C%7Ca%7C%7C%7C%7CCUR%7Cend; cookie_consent=0; _pxhd=pQ0i1qD3gO9RlCm-Qfbk7ex53Eb3wBtcFzsAfwEQoicUg7jdRsH-mEzrSH1SG7Rvt3A5TF4vo8yBqZp5hv1gcg==:sHzVQ4MKlWwCoLBqXoH01OZPTwFpn99jsm2wsZPanNGM8M0LynkKYWc7EXs58V2PxoOETXiNLqkuuEdJNczRPSHDlWL1KlwxQLExHfQPRMw=; mrkloc=Czech%2BRepublic%7CCZ%7C%7CCzech%2BRepublic-CZ-%3B%20path%3D%2F%3B%20domain%3Dwine-searcher.com%3B%20expires%3DTue%2C%2031-Dec-2030%2000%3A00%3A00%20GMT; cookie_enabled=true; adin=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MzE5MjM3MDguODI0MzQ5LCJleHAiOjE3NzIwOTk3MDguODI0MzQ5LCJ1aWQiOm51bGwsInVlYSI6bnVsbCwidWFjZCI6bnVsbH0.Ozs-xuG_qYmrrEqtMHPIX0xpJ2ZRrPPMnvsuchzLw44; fflag=flag_ab_testing%3A0%2Cend; search=start%7Cde%2Bpibarnon%2Bbandol%2Bprovence%2Bfrance%7C1%7Cany%7CUSD%7C%7C%7C%7C%7C%7C%7C%7C%7Ce%7Ci%7C%7C%7CN%7C%7Ca%7C%7C%7C%7CCUR%7Cend; COOKIE_ID=D2PHC36FKQ100SM; ID=D2PHC36FKQ100SM; IDPWD=I74562238; _csrf=VUcPL0eeV-P9V5MSdJLFvPxdDf1gfFB4; _pxhd=PpOEZ9k9lVIoAQtQc1xu9lCkOsQpB8LPL24rZmrzkMjaXUi3Ro-2rNEdJ3Zh5/bqFnrjfu2W60irbOhncxehhQ==:Z6jiUSjviSc9Lr0keW5-T2ZopQ/q2izzrgrT2QKtf/ChP1OTnFVZc-xgDWJCSdiYAbVLcEZM7kinlDt1kg3SYgKmeG5-pOArFMhrKNSefyw=; cookie_consent=0; find_tab=%23t1; user_status=A%7C",
    # "Upgrade-Insecure-Requests": "1",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-User": "?1",
    # "DNT": "1",
    # "Sec-GPC": "1",
    # "Priority": "u=0, i",
    # "Pragma": "no-cache",
    # "Cache-Control": "no-cache",
    # "TE": "trailers",
}


async def custom_headers(
    *,
    browser_type_name: str,
    playwright_request: playwright.async_api.Request,
    scrapy_request_data: dict,
) -> Dict[str, str]:
    headers = await playwright_request.all_headers()
    headers.update(REQUEST_HEADERS)
    return headers


class BotDebugSpider(scrapy.Spider):
    name = "bot_debug"
    allowed_domains = [
        "antoinevastel.com",
        "deviceandbrowserinfo.com",
        "wine-searcher.com",
    ]
    start_urls = [
        # "https://deviceandbrowserinfo.com/info_device",
        # "https://arh.antoinevastel.com/bots/areyouheadless",
        # "https://arh.antoinevastel.com/bots/",
        "https://www.wine-searcher.com/find/de+pibarnon+bandol+provence+france",
    ]

    custom_settings = {
        "LOG_LEVEL": "INFO",
        "USER_AGENT": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
            "scrapers.middlewares.retry.RetryMiddleware": 550,
        },
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
        "PLAYWRIGHT_PROCESS_REQUEST_HEADERS": custom_headers,
    }

    def start_requests(self):
        """Initiate a request using Playwright."""
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse,
                # headers=REQUEST_HEADERS,
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
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                        viewport={"width": 1920, "height": 1080},
                        geolocation={"latitude": 37.7749, "longitude": -122.4194},
                        permissions=["geolocation"],
                        java_script_enabled=True,
                    ),
                    playwright_page_goto_kwargs=dict(
                        wait_until="networkidle",
                    ),
                ),
            )

    async def parse(self, response):
        try:
            """Parse the page content after clicking the button and taking a screenshot."""
            page = response.meta["playwright_page"]
            context = page.context

            print("Context:", context)

            # Apply stealth mode to reduce detection
            # await stealth_async(page)

            # Inject a script to override navigator.userAgentData before any page scripts run
            await page.add_init_script(
                """
                Object.defineProperty(navigator, 'userAgentData', {
                    get: () => ({
                        brands: [
                            { brand: "Google Chrome", version: "115" },
                            { brand: "Chromium", version: "115" },
                            { brand: "Not A;Brand", version: "99" }
                        ],
                        mobile: false,
                        platform: "macOS"
                    })
                });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                Object.defineProperty(navigator, 'platform', { get: () => 'MacIntel' });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 4 });
                """
            )

            # Set custom headers using Playwright's API
            await page.set_extra_http_headers(REQUEST_HEADERS)

            # Delete the navigator.webdriver property
            await page.evaluate("delete navigator.webdriver")

            # Randomize browser fingerprints
            await page.evaluate(
                """
                Object.defineProperty(navigator, 'userAgentData', {
                    get: () => ({
                        brands: [
                            { brand: "Google Chrome", version: "115" },
                            { brand: "Chromium", version: "115" },
                            { brand: "Not A;Brand", version: "99" }
                        ],
                        mobile: false,
                        platform: "macOS"
                    })
                });
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                Object.defineProperty(navigator, 'platform', { get: () => 'MacIntel' });
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 4 });
                """
            )

            brands = await page.evaluate("navigator.userAgentData.brands")
            logging.info(f"navigator.userAgentData.brands: {brands}")

            user_agent = await page.evaluate("navigator.userAgent")
            logging.info(f"Current User-Agent: {user_agent}")

            # Wait for the page to load
            await page.wait_for_selector("body")
            await page.screenshot(path="screenshot.png", full_page=True)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
        finally:
            await page.close()
