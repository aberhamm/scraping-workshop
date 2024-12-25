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

    splash:init_cookies({
        {
            name = "client_cache_key",
            value = "BcxhmgIUcgmqV7HyJWoWN7UP6CyUfKbLQoMsB58WQ10Cm%2FQ6ErxoHPoLL4jAv2%2BzzbCZRSq4C5m47KoZhs%2FBoVPbu1DNh%2FK7TSxkol9yXc1uLFw5l%2FJvvEWIzWIype%2B7F4Oeu%2FbPF%2FX8qLtPHXWekW5b--XxBcZz4ZRXTlp6cy--GXijX8R9NpJy1QvNt954Kg%3D%3D",
            domain = "www.vivino.com",
            path = "/",
            expires = "1732242296",
            httpOnly = true,
            secure = true
        },
        {
            name = "first_time_visit",
            value = "ioOdMAY0wMiW7Mes%2FZd6zjDOJZL%2BEic8NW0q2Iy%2FCH7D4SVeLLro7S8Q4VPj%2F54YSniFVkcMgN86PIzSQHub%2BMYkSqtiOKBeizNfHWo5lP5WMgrIHyeVWxRjhE8FKDLf1JU%3D--ZHRY7MHo98lRNbU4--w9CoyFWeRjnuw%2BFOZm%2B6LA%3D%3D",
            domain = "www.vivino.com",
            path = "/",
            expires = "1766715897",
            httpOnly = true,
            secure = true
        },
        {
            name = "anonymous_tracking_id",
            value = "%2F4N3o8a9GyAICTOZcuRmwMVdnPBKzmlgalrSTbWlVuOSJ%2FePGz5TuYT%2Fj%2B3A0SpAcQ%2BFm%2BgDKCCwGjI4w%2FUMWB6nSAV6qTKCzHUx%2FM%2Fd71gVQRS8tSmuqifibATt5GGeTdCFhDR%2FKwnfkqH0lsQcEDNCLwVH0TnfYrJWMzlX%2F2Po0ZS1D6YZn4tzXKMr1Ls16uK7--aZTg2L2Yqqg%2FcRO9--pWEgy74qXQmY8sKFtj6BkQ%3D%3D",
            domain = "www.vivino.com",
            path = "/",
            expires = "1766715897",
            httpOnly = true,
            secure = true
        },
        {
            name = "eeny_meeny_explorer_card_v2",
            value = "pDon4bA2iARqMRjr2mpdgwZIWs67ZyiaPm2j0GxJj2khXFUlf%2Frycbkv36ELJdyKIvV6eh8doRoijl6ns1F0Ng%3D%3D",
            domain = "www.vivino.com",
            path = "/",
            expires = "1734747896",
            httpOnly = true,
            secure = true
        },
        {
            name = "csrf_token",
            value = "xf13YVJ9Pc8pe2NceTSgewnkmtpyaUm5nbMeQpHlr6vMPiSrXTL7Bp-s9jm03mjpusPPn-jlpWt0NsP_j5NXdQ",
            domain = "www.vivino.com",
            path = "/",
            expires = "1732242466",
            httpOnly = true,
            secure = true
        },
        {
            name = "_ruby-web_session",
            value = "2F%2FLm5h4gxuBR695iK8B1cyTMRof64fTFsO%2Bb5TaFmTCfPDDLMJqn4wfPeQEcBGUwp70UGKRsAgIySg1aQ%2B2JVPARBvD5KsSKdb21%2F0f05KQD1YHkCI2ZrrE46GEvXx0yLy1rjguArV235ShnfFz1T1XEX%2FENDU%2BgzT7TrXbQPyENfYGKRTUdZznNg6ahQZMV%2BfwAfnXhOxINzGpPwLX1AulgA%2BLmKoIS8dw2A7rMtAoPF%2Bb%2BzYto0sP8ZKPMHTpRpWdt88z3j2VLTq%2BN7CAj9fvavppt7uLhgxlB3JhneAYqZn4OjfITVwyMVrF5bzHoMH68FEK3ZuyeStX3tgkAQdJP5U1RZniwPZ%2FqFccPYbVbw%2Bix162oJiVS34DtJKN%2BKSyRL%2FWVGmL7%2FBYYlJaB4Vu6NsLTjcH1Epk1%2BRm2HzmwnJqQ2%2FkPYBKAIXxjii4Uc%2BvobzjMJbS3C%2BZOp8o9faFNl8k%2B3plhf3Wl3Cmv%2BFjHWpmqehL0YKgWD4bbRR4LA5Q1BzSJRMoNRE%3D--8GKWQy4Y%2FyDw3PwS--DVZwauBN45pR5ht%2FRItW%2Fg%3D%3D",
            domain = "www.vivino.com",
            path = "/",
            expires = "1763692066",
            httpOnly = true,
            secure = true
        },
        {
            name = "euconsent-v2",
            value = "CP3FdEAQIcLAAAHABBENBQFsAP_gAEPgAAZQKMtX_H__bW9r8X73aft0eY1P99j77uQxBhfJE-4FzLvW_JwXx2ExNA36tqIKmRIEu3bBIQNlHJHUTVigaogVryHMakWchTNKJ6BkiFMRO2dYCF5vm4tj-QKY5_p993dx2D-t_dv83dzyz81Hn3f5_2e0eLCdQ58tDfv9bROb-9IPd_78v4v0_l_rk2_eT1n_tevr7D--ft87_XW-9_fff79LlAACCjIBJhoVEAfYEhIQaBhFAgBUFYQEUCgAAAEgaICAEwYFOwMAF1hIgBACgAGCAEAAIMgAQAAAQAIRABIAUCAACAQKAAEAAAQCAAgYAAQAWAgEAAIDoGKYEECgWECRmREKYEIUCQQEtlQgkBQIK4QhFngAQCImCgAQAAAKwABAWCwGJJASoSCBLqDaAAAgAQCiECoQSemAAYEjZag8EDaMrSAMDQAAgAAA.f_wACHwAAAAA",
            domain = ".vivino.com",
            path = "/",
            httpOnly = false,
            secure = false
        }
    })
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
