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

    splash.images_enabled = false

    -- Navigate to the target URL
    local ok, err = splash:go(splash.args.url)
    if not ok then
        return {error = "Navigation failed: " .. err}
    end

    -- Poll for the CSS selector to appear (timeout after 10 seconds)
    local max_retries = 50  -- Retry up to 50 times
    local delay = 0.2       -- 200ms between retries
    local selector = args.wait_for_selector
    local element_found = false

    for i = 1, max_retries do
        element_found = splash:evaljs("document.querySelector('" .. selector .. "') !== null")
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
    ]], args.css_content) -- Escape quotes in CSS
    splash:evaljs(css_injection)

    -- Inject custom JS
    splash:evaljs(args.js_content)
    splash:wait(2)

    local content = splash:evaljs("document.querySelector('main').innerText")

    -- Adjust viewport to capture the full page
    splash:set_viewport_full()

    -- Return HTML and screenshot for debugging
    return {
        html = splash:html(),
        png = splash:png(),
        jpeg = splash:jpeg(),
        content = content,
    }
end
