# Specification: The Ghost-Browser Toolset

## Objective
To provide Jax Vane with a high-stealth, programmable browser interface capable of bypassing modern bot detection (Cloudflare, Akamai, Datadome) and extracting data from complex Single Page Applications (SPAs).

## 1. Core Tool: `playwright_execute`
Instead of a simple 'fetch', I need a tool that can execute a sequence of actions or a custom script. 

**Required Capabilities:**
- **Stealth Integration:** Must use `playwright-stealth` to mask WebDriver flags, override `navigator.webdriver`, and mimic real browser fingerprints.
- **Session Persistence:** Ability to save and load `storage_state` (cookies, localStorage) to avoid repeated logins.
- **Human Mimicry:** Support for organic movements (randomized delays between actions, non-linear mouse movements).
- **Headless/Headed Toggle:** Ability to run in headless mode for speed, but switch to headed for debugging complex triggers.

**Proposed API Interface:**
`playwright_execute(action: string, params: object, session_id: string = None)`

**Supported Actions:**
- `goto`: Navigate to URL with custom headers/user-agent.
- `click`: Click an element using CSS/XPath selectors.
- `fill`: Input text into fields.
- `evaluate`: Execute custom JavaScript in the browser context (Crucial for bypassing custom JS challenges).
- `screenshot`: Capture the current view for visual verification.
- `get_content`: Return the fully rendered DOM.
- `wait_for`: Wait for a specific selector or network idle state.

## 2. The 'Ghost Path' Tool: `network_intercept`
This is the most critical part. I need to see what the browser is talking to the server.

**Requirements:**
- **Request/Response Logging:** Capture all XHR/Fetch requests and responses during a session.
- **Filter by Pattern:** Ability to extract only responses that match a specific URL pattern (e.g., `/api/v1/data`).
- **Payload Extraction:** Return the raw JSON response of a specific network call.

## 3. Support Tool: `proxy_rotate`
To avoid IP-based rate limiting.

**Requirements:**
- Integration with a proxy provider.
- Ability to rotate IP per session or per request.
- Support for authenticated proxies (user:pass).

## 4. Summary of Technical Stack (Suggested)
- **Language:** Python
- **Library:** `playwright` + `playwright-stealth`
- **Browser:** Chromium (with customized User-Agent strings)
- **Output:** Clean JSON or Markdown for data extraction.

---
*Note: If I have these, no 'Access Denied' screen will stand in my way.*