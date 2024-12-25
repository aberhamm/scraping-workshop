from datetime import datetime
import os
from urllib.parse import urlparse
import scrapy
from scrapy_splash import SplashRequest
import base64
import requests
import logging

PROXY_CONFIG = {
    "host": "brd.superproxy.io",
    "port": 22225,
    "username": "brd-customer-hl_a0ff3a6d-zone-isp_proxy1",
    "password": "0kfdfxpqlon9",
}

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "close",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}


def ensure_output_dir(output_dir="./output"):
    """
    Ensure the output directory exists.
    """
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def generate_filename(response, extension, output_dir="./output"):
    """
    Generate a timestamped filename based on the domain and file extension.
    """
    domain = parse_domain(response.url)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"{domain}_{timestamp}.{extension}")


def save_to_file(content, filename, mode="wb"):
    """
    Save content to a file. Supports both binary and text content.
    """
    try:
        with open(filename, mode) as f:
            f.write(content)
        logging.info(f"Saved content to {filename}")
    except Exception as e:
        logging.info(f"Failed to save file {filename}: {e}", level=logging.ERROR)


def process_image_response(response, image_format):
    """
    Process and save the image (PNG or JPEG) from the response.
    """
    image_data = response.data.get(image_format)

    if not image_data:
        logging.info(
            f"No {image_format.upper()} data found in response from {response.url}",
            level=logging.WARNING,
        )
        return

    # Decode the image data
    try:
        image_binary = base64.b64decode(image_data)
    except Exception as e:
        logging.info(
            f"Failed to decode {image_format.upper()} image data from {response.url}: {e}",
            level=logging.ERROR,
        )
        return

    # Ensure directory exists and save the image
    output_dir = ensure_output_dir()
    filename = generate_filename(response, image_format, output_dir)
    save_to_file(image_binary, filename, mode="wb")


def process_html_response(response):
    """
    Process and save the HTML content from the response.
    """
    try:
        html_content = response.body.decode("utf-8")
    except Exception as e:
        logging.info(
            f"Failed to decode HTML content from {response.url}: {e}",
            level=logging.ERROR,
        )
        return

    # Ensure directory exists and save the HTML
    output_dir = ensure_output_dir()
    filename = generate_filename(response, "html", output_dir)
    save_to_file(html_content, filename, mode="w")


def process_text_response(response):
    """
    Process and save the text content from the response.
    """
    if "content" not in response.data:
        logging.info(
            f"No text content found in response from {response.url}",
            level=logging.WARNING,
        )
        return

    text_content = response.data["content"]

    # Ensure directory exists and save the text
    output_dir = ensure_output_dir()
    filename = generate_filename(response, "txt", output_dir)
    save_to_file(text_content, filename, mode="w")


def parse_domain(url):
    """
    Parse the domain from the given URL.
    """
    domain = None
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split(".")
    if domain_parts[0] in [
        "www",
        "m",
    ]:
        domain = ".".join(domain_parts[1:])
    else:
        domain = parsed_url.netloc
    domain = domain.replace(".", "_")
    return domain


def load_script(folder, domain):
    """
    Load a script from the given folder and domain-specific filename.
    If the domain-specific script does not exist, attempt to load a default script.
    """
    logging.info(f"Loading {folder} script for {domain}")
    script_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), f"../scripts/{folder}")
    )

    # Domain-specific script path
    domain_script_path = os.path.join(
        script_dir,
        f"{domain}.{'js' if folder == 'js' else 'lua' if folder == 'lua' else 'css'}",
    )

    # Default script path
    default_script_path = os.path.join(
        script_dir,
        f"default.{'js' if folder == 'js' else 'lua' if folder == 'lua' else 'css'}",
    )

    # Attempt to load domain-specific script
    if os.path.exists(domain_script_path):
        logging.info(f"Loaded {folder} script for {domain}")
        with open(domain_script_path, "r", encoding="utf-8") as file:
            return file.read()

    # Fallback to default script if domain-specific script is not found
    elif os.path.exists(default_script_path):
        logging.warning(f"No {folder} script found for {domain}. Using default script.")
        with open(default_script_path, "r", encoding="utf-8") as file:
            return file.read()

    # No script found
    logging.warning(f"No {folder} script found for {domain} or default. Skipping.")
    return None


def process_request_log(requests_log):
    """
    Process the outgoing requests logged by Splash.
    """
    for key, req in requests_log.items():  # Iterate over the dictionary items
        logging.info(f"Request - URL: {req['url']}, Method: {req['method']}")


def process_response_log(responses_log):
    """
    Process the incoming responses logged by Splash.
    """
    for key, res in responses_log.items():  # Iterate over the dictionary items
        logging.info(f"Response - URL: {res['url']}, Status: {res['status']}")


class SplashSpider(scrapy.Spider):
    # define the name of the spider
    name = "splash_spider"

    start_urls = [
        # "https://www.wine-searcher.com/find/de+pibarnon+bandol+provence+france#t2",
        # "https://deviceandbrowserinfo.com/info_device",
        # "https://www.vivino.com",
        # "https://www.vivino.com/NL/en/dom-perignon-p2-plenitude-brut-champagne/w/3102815?year=2006&price_id=37282910"
        "https://www.tripadvisor.com/Hotels-g187323-Berlin-Hotels.html"
    ]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "DEFAULT_REQUEST_HEADERS": DEFAULT_REQUEST_HEADERS,
        "LOG_LEVEL": "INFO",
        "RETRY_ENABLED": True,
        "RETRY_TIMES": 3,
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 407, 408],
        "HTTPERROR_ALLOW_ALL": True,
        # Splash settings
        "SPLASH_URL": "http://localhost:8050",  # Splash IP
        # Middleware
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_splash.SplashCookiesMiddleware": 723,
            "scrapy_splash.SplashMiddleware": 725,
            "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
        },
        # Duplicate filter and cache
        "SPIDER_MIDDLEWARES": {
            "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
        },
        "DUPEFILTER_CLASS": "scrapy_splash.SplashAwareDupeFilter",
        "HTTPCACHE_STORAGE": "scrapy_splash.SplashAwareFSCacheStorage",
    }

    def start_requests(self):
        for url in self.start_urls:
            domain = parse_domain(url)

            # Load scripts dynamically
            css = load_script("css", domain)
            js = load_script("js", domain)
            lua_script = load_script("lua", domain)

            # set up Splash arguments
            args = {
                "html": 1,
                "png": 1,
                "render_all": 1,
                "wait": 1,
                "timeout": 20,
                "url": url,
                "lua_source": lua_script,
                "wait_for_selector": "#find-tab-info",
                "headers": DEFAULT_REQUEST_HEADERS,
                "proxy_config": PROXY_CONFIG,
                "allowed_content_types": "*",
                "js_source": "element = document.querySelector('h1').innerHTML = 'The best quotes of all time!'",
                # "allowed_content_types": [
                #     "text/html",
                #     "image/png",
                #     "image/jpeg",
                #     "text/css",
                #     "application/javascript",
                # ],
            }

            if css:
                args["css_content"] = (
                    css.replace(" ", "").replace("\n", "").replace("\t", "")
                )
            if js:
                args["js_content"] = js

            # make a request using Splash and pass the response to the parse method
            yield SplashRequest(
                url,
                self.parse,
                endpoint="execute",  # Use "execute" for Lua scripts
                args=args,
                # meta={"proxy": self.proxy},
                # headers=headers,
                # cache_args=["lua_source"],
            )

    def parse(self, response):
        """
        Main parsing logic. Checks and processes all available response data types
        while logging which were provided and which were not.
        Handles multiple image formats if both are provided.
        """
        # Initialize a dictionary to track provided data types
        provided = {
            "png": "png" in response.data,
            "jpeg": "jpeg" in response.data,
            "content": "content" in response.data,
            "html": bool(response.body),
        }

        # Log the availability of each type
        logging.info(f"Response data availability: {provided}")

        # Process images (handle both PNG and JPEG if provided)
        if provided["png"]:
            process_image_response(response, "png")
        if provided["jpeg"]:
            process_image_response(response, "jpeg")

        # Process text content if available
        if provided["content"]:
            process_text_response(response)

        # Process HTML body if available
        if provided["html"]:
            process_html_response(response)

        # Log a warning if no recognized data type was provided
        if not any(provided.values()):
            logging.info(
                f"No recognized data types found in response from: {response.url}",
                level=logging.WARNING,
            )

        requests_log = response.data.get("requests", [])
        responses_log = response.data.get("responses", [])

        # Process requests and responses log
        process_request_log(requests_log)
        process_response_log(responses_log)
