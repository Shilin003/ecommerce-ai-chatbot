import json
from playwright.sync_api import sync_playwright

def scrape_amazon_product(product_url):
    with sync_playwright() as p:
        # Launch browser with human-like configurations
        browser = p.chromium.launch(headless=True)
        
        # Spoof user-agent headers to bypass basic anti-bot firewalls
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        page = context.new_page()
        print(f"Navigating to Amazon listing: {product_url}...")
        
        # Go to URL and wait for network activity to settle down
        page.goto(product_url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000) # Give elements 2 seconds to fully render
        
        # Extract data using Amazon's global element IDs
        try:
            # 1. Product Title (Amazon uses ID: productTitle)
            title = page.locator("#productTitle").text_content()
            title = title.strip() if title else "N/A"
            
            # 2. Main Product Image (Amazon uses ID: landingImage)
            image_element = page.locator("#landingImage")
            image_url = image_element.get_attribute("src") if image_element.count() > 0 else "N/A"
            
            # 3. Product Price (Amazon selectors change based on layout; fallback logic is safer)
            price = "N/A"
            price_selectors = ["span.a-price-whole", "#priceblock_ourprice", "#priceblock_dealprice", "span.a-offscreen"]
            for selector in price_selectors:
                element = page.locator(selector)
                if element.count() > 0:
                    price = element.first.text_content().strip()
                    break
            
            # 4. Feature Details / Bullet Points (Amazon uses ID: feature-bullets)
            bullets = []
            bullet_elements = page.locator("#feature-bullets ul li span.a-list-item").all_text_contents()
            for bullet in bullet_elements:
                cleaned_bullet = bullet.strip()
                if cleaned_bullet:
                    bullets.append(cleaned_bullet)

            # Package into a structured data directory
            product_data = {
                "title": title,
                "price": price,
                "image_url": image_url,
                "details": bullets
            }
            
            print("Successfully extracted data item map!")
            return product_data

        except Exception as e:
            print(f"Data extraction failed: {e}")
            return None
        finally:
            browser.close()

# 🧪 Run an instant test case locally
if __name__ == "__main__":
    # Sample Amazon Listing URL (You can swap this with any direct product link)
    target_url = "https://www.amazon.com/dp/B0CX21C8T3" 
    
    scraped_result = scrape_amazon_product(target_url)
    
    if scraped_result:
        # Save structured results to a JSON file for your frontend shop page
        with open("amazon_product.json", "w", encoding="utf-8") as f:
            json.dump(scraped_result, f, indent=4, ensure_ascii=False)
        print("\nScraped Content Preview:")
        print(json.dumps(scraped_result, indent=2, ensure_ascii=False))