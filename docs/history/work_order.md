# ✅ COMPLETED: Implementation of `download_file` Tool

**Status:** Verified and Proven.

## 1. Objective
Implement a new tool that allows the agent to download binary files (specifically PDFs) from remote URLs and save them directly to the local filesystem without passing the file content through the LLM's response channel.

## 2. Technical Specification

### Tool Signature
`download_file(url: string, path: string, headers: object = None, cookies: object = None)`

### Parameters
- **`url` (string):** The absolute URL of the file to be downloaded.
- **`path` (string):** The absolute or relative path where the file should be stored on the local disk (e.g., `/taxes/cornu_1561/general/electricity/bill_jan.pdf`).
- **`headers` (object, optional):** A dictionary of HTTP headers to be sent with the request. This is critical for simulating browsers (`User-Agent`) and providing `Referer` information to avoid being blocked by government portals.
- **`cookies` (object, optional):** A dictionary of cookies to be sent with the request. This is essential for maintaining sessions in portals like Oracle APEX or Virtual Offices.

## 3. Functional Requirements

### A. Binary Stream Handling
- The tool **MUST NOT** read the file content into memory as a string.
- It must implement a **streaming download** (chunked writing) to handle files of various sizes (from a few KB to several MB) without causing memory overflows or token saturation in the agent's context.

### B. Filesystem Integration
- The tool must ensure that the destination directory exists before attempting to write the file. If the directory does not exist, it should be created automatically.
- It must overwrite existing files if the path is identical, or handle naming collisions as per system policy.

### C. Error Handling & Returns
- **Success:** Return `'OK'` upon successful download and verification of the file on disk.
- **Failure:** Return `'ERR: <detailed_message>'` in case of:
    - HTTP Errors (403 Forbidden, 404 Not Found, 500 Internal Server Error).
    - Connection timeouts.
    - Disk write permissions errors.
    - Invalid URL format.

## 4. Use Case Example
**Scenario:** Downloading a tax bill from a session-protected portal.

**Call:**
`download_file(
    url="https://portal.gov.ar/download/bill_123.pdf",
    path="taxes/san_andres_129/municipal/2024_bill.pdf",
    headers={"User-Agent": "Mozilla/5.0...", "Referer": "https://portal.gov.ar/session"},
    cookies={"SESSIONID": "abc123xyz"}
)`

## 5. Rationale
Currently, the `api_request` tool is limited to text-based responses. Attempting to download binary PDFs through it leads to data corruption and token exhaustion. This tool is the missing link to achieve a fully autonomous "Harvest Module" for the Tax & Utility Hub.