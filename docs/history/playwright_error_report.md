# Bug Report: `browser_execute` Serialization Error

## Error Summary
**Tool:** `browser_execute`  
**Error Message:** `ERR: Unexpected error in 'browser_execute': Object of type coroutine is not JSON serializable`

## Technical Analysis
The error indicates a failure in the tool's internal execution wrapper. Specifically, the tool is calling an `async` function (a coroutine) but is attempting to return the coroutine object itself rather than the *result* of the awaited execution.

In Python, when an `async def` function is called, it returns a coroutine object. If the wrapper responsible for executing this tool does not `await` the function or run it via an event loop (e.g., `asyncio.run()`), the system attempts to serialize the coroutine object into JSON to send the response back to the agent. Since coroutines are not JSON-serializable, the process crashes with the reported error.

## Operational Impact
This failure is a **critical blocker** for the current acquisition phase ("The Ghost Path"). The target portals exhibit the following characteristics that make `browser_execute` indispensable:

1. **Cloudflare Protection (Edemsa):** Raw HTTP requests via `api_request` are triggering 403 Forbidden responses. A headless browser with stealth plugins is required to pass the TLS fingerprinting and JS challenges.
2. **JS-Heavy Rendering (AYSAM):** The portal relies on client-side JavaScript to populate account data and generate download links. `render_web_page` (ELinks) cannot execute the JS required to reach the PDF endpoints.
3. **Session State & Oracle APEX (Municipal/ATM):** These portals use complex session tokens and state management (Oracle APEX) that require a full browser context to maintain persistence and trigger the binary PDF stream.

## Expected Behavior
The tool should:
1. Receive the action and parameters.
2. Execute the browser sequence within an asynchronous event loop.
3. `await` the completion of the action.
4. Return the resulting data (string, boolean, or object) as a JSON-serializable response.

## Suggested Fix
Ensure that the tool's entry point is properly awaiting the browser call. Example:

```python
# Incorrect
result = browser_action(params)
return json.dumps(result) # Crashes here because result is a coroutine

# Correct
import asyncio
result = asyncio.run(browser_action(params))
return json.dumps(result)
```