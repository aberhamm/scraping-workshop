function main(splash, args)
    -- Set headers to mimic the successful curl request
    splash:on_request(function(request)
        -- Set custom headers if provided
        if args.headers then
            for header, value in pairs(args.headers) do
                request:set_header(header, value)
            end
        end

        -- Set proxy configuration
        request:set_proxy{
            type = "HTTP",
            host = args.proxy_config.host,
            port = args.proxy_config.port,
            username = args.proxy_config.username,
            password = args.proxy_config.password,
        }
    end)
    -- Table to store request and response logs
    local request_log = {}
    local response_log = {}

    -- Log outgoing requests
    splash:on_request(function(request)
        table.insert(request_log, {url = request.url, method = request.method})
    end)

    -- Log incoming responses
    splash:on_response(function(response)
        table.insert(response_log, {url = response.url, status = response.status})
    end)

    -- splash:init_cookies({
    splash.js_enabled = true
    -- splash.images_enabled = false

    -- Navigate to the target URL
    local ok, err = splash:go(splash.args.url)
    if not ok then
        return {error = "Navigation failed: " .. err}
    end

    -- Wait for the page to load
    splash:wait(2)

    -- Poll for the CSS selector to appear (timeout after 10 seconds)
    local max_retries = 50  -- Retry up to 50 times
    local delay = 0.2       -- 200ms between retries
    local selector = args.wait_for_selector
    local element_found = false

    for i = 1, max_retries do
        element_found = splash:evaljs("document.querySelector('body') !== null")
        if element_found then
            break
        end
        splash:wait(delay)
    end

    -- Inject custom CSS
    local css_injection = string.format([[
        var style = document.createElement('style');
        style.type = 'text/css';
        style.appendChild(document.createTextNode('%s'));
        document.head.appendChild(style);
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.innerText = `
                document.body.style.fontFamily = 'Arial, sans-serif';
                let header = document.createElement('h1');
                header.textContent = 'Hello from Lua!';
                document.body.prepend(header);
        `;
        document.body.appendChild(script);
    ]], args.css_content)
    splash:evaljs(css_injection)

    -- Inject custom JS
    splash:evaljs(args.js_content)
    splash:wait(2)

    -- Scroll down the page
    local scroll_height = splash:evaljs("document.body.scrollHeight")
    local current_position = 0
    splash.scroll_position = {x = 0, y = 0}

    while current_position < scroll_height do
        current_position = current_position + 500  -- Scroll step size
        splash.scroll_position = {x = 0, y = current_position}  -- Correct method call
        splash:wait(1)  -- Allow content to load
        scroll_height = splash:evaljs("document.body.scrollHeight")
    end

    local content = splash:evaljs("document.querySelector('body').innerText")

    -- Adjust viewport to capture the full page
    splash:set_viewport_full()

    -- Return HTML and screenshot for debugging
    return {
        html = splash:html(),
        png = splash:png(),
        -- jpeg = splash:jpeg(),
        -- content = content,
        requests = request_log,
        responses = response_log,
    }
end
