from fastapi import FastAPI
from playwright.async_api import async_playwright

app = FastAPI()

@app.get("/interact/")
async def interact(command: str = "", website: str = "google"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Ensure visibility
        page = await browser.new_page()

        try:
            command_lower = command.lower()

            # Handle unrecognized commands
            if not any(keyword in command_lower for keyword in ["open", "search for", "click the", "login"]):
                return {"error": f"Command '{command}' not recognized. Please provide a valid command."}

            # Open a website
            if "open" in command_lower:
                site = command_lower.replace("open", "").strip()
                if site:
                    site_url = f"https://www.{site}.com" if "." not in site else f"https://{site}"
                    await page.goto(site_url)
                    await page.wait_for_load_state("domcontentloaded")
                    # Stay open for a while
                    await page.wait_for_timeout(60000)  # Stay open for 60 seconds
                    return {"message": f"Opened {site_url}"}
                return {"error": "No site specified to open"}

            # Search for a query
            elif "search for" in command_lower:
                query = command_lower.replace("search for", "").strip()

                if not query:
                    return {"error": "No query specified for search"}
                
                search_urls = {
                    "google": f"https://www.google.com/search?q={query}",
                    "bing": f"https://www.bing.com/search?q={query}",
                    "amazon": f"https://www.amazon.com/s?k={query}",
                    "youtube": f"https://www.youtube.com/results?search_query={query}"
                }

                # Open search result page, regardless of the website
                if website:
                    search_url = f"https://www.{website}.com/search?q={query}"  # Generic search URL
                    await page.goto(search_url)
                    await page.wait_for_load_state("domcontentloaded")
                    # Stay open for a while
                    await page.wait_for_timeout(60000)  # Stay open for 60 seconds
                    return {"message": f"Searched for '{query}' on {website}"}
                return {"error": f"Website {website} not supported for search"}

            # Login to Gmail (for demonstration purposes, real login automation is complex)
            elif "login" in command_lower and "gmail" in command_lower:
                await page.goto("https://mail.google.com/")
                await page.wait_for_selector("input[type='email']")  # Wait for the email field
                # For demonstration, simulate login by entering a dummy email
                await page.fill("input[type='email']", "dummyemail@gmail.com")
                await page.click("button[jsname='LgbsSe']")  # Click the 'Next' button
                await page.wait_for_selector("input[type='password']")  # Wait for password field
                await page.fill("input[type='password']", "dummyPassword123")  # Enter dummy password
                await page.click("button[jsname='LgbsSe']")  # Click 'Next' again
                await page.wait_for_timeout(60000)  # Stay open for 60 seconds to simulate login
                return {"message": "Attempting to log in to Gmail (actual login requires valid credentials)"}

            # Click a specific search result
            elif "click the" in command_lower and "result" in command_lower:
                # Wait for search result elements to load (using a generic tag for search results)
                await page.wait_for_selector("h3")  # Common for search results, can be modified
                results = await page.query_selector_all("h3")
                

                # Ensure there are enough results
                if len(results) >= 2:
                    await results[1].click()  # Click the second result (index 1)
                    # Stay open for a while
                    await page.wait_for_timeout(60000)  # Stay open for 60 seconds
                    return {"message": "Clicked on the second search result"}
                else:
                    return {"error": "Not enough search results found to click the second one."}

            return {"error": "Unknown command"}

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
