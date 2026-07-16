import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

chrome_path = os.getenv("CHROME_EXECUTABLE_PATH")

url_list = [
    "https://www.digikala.com/product/dkp-21679945/",
    "https://www.digikala.com/product/dkp-340776/",
    "https://www.digikala.com/product/dkp-5715766/", 
    "https://www.digikala.com/product/dkp-223806", 
    "https://www.digikala.com/product/dkp-17918956",
    "https://www.digikala.com/product/dkp-6785396", 
    "https://www.digikala.com/product/dkp-7192610", 
    "https://www.digikala.com/product/dkp-2067210",
    "https://www.digikala.com/product/dkp-3827346", 
    "https://www.digikala.com/product/dkp-17918956/"
]

def extract_and_print_comments(page, page_number):
    comments = page.locator("#commentSection article.br-list-vertical-no-padding-200").all()    
    print(f"|Page: {page_number} | Comments count: {len(comments)}|")
    print("=" * 100)

    for comment in comments:
        try:
            more_text_btn = comment.locator("span:has-text('ادامه')").first
            if more_text_btn.is_visible():
                try:
                    more_text_btn.click(timeout=1500)
                    page.wait_for_timeout(300)
                except Exception:
                    pass

            name = comment.locator("p.text-body1-strong-compact").first.inner_text().strip()
            text = comment.locator("p.text-body-1.text-neutral-900").first.inner_text().strip()

            buyer_locator = comment.locator("p:has-text('خریدار')").first
            is_buyer = 1 if buyer_locator.is_visible() else 0

            expert_locator = comment.locator("div:has-text('صاحب‌نظر')").first
            is_expert = 1 if expert_locator.is_visible() else 0

            try:
                filled_stars = comment.locator("img[src*='star-fill']").all()
                star = len(filled_stars)
            except Exception:
                star = 0

            print(f"Name: {name} | Star: {star} | Is buyer: {is_buyer} | Is expert: {is_expert}")
            print(f"Text: {text}")
            print("-" * 100)
        except Exception as e:
            pass

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, executable_path=chrome_path)
        page = browser.new_page()
        
        for index, url in enumerate(url_list):
            print(f"\n-- link: {index + 1} | url: {url} --")
            try:
                page.goto(url)
                page.wait_for_timeout(4000)

                for scroll_pos in range(2000, 4000, 400):
                    page.evaluate(f"window.scrollTo(0, {scroll_pos});")
                    page.wait_for_timeout(1000)

                comments_tab = page.locator("li[data-cro-id='pdp-scroll-menu']").filter(has_text="دیدگاه‌ها").first
                if comments_tab.is_visible():
                    comments_tab.click(force=True)
                    print("-- Clicked on Comments Tab -- ")
                    page.wait_for_timeout(3000)

                page.evaluate("window.scrollBy(0, 800);")
                page.wait_for_timeout(2000)

                more_comments_btn = page.locator("p.text-secondary-500:has-text('دیدگاه دیگر')").first
                if more_comments_btn.is_visible():
                    try:
                        more_comments_btn.click(force=True, timeout=5000)
                        print("-- Successfully => More Comments --\n" + "=" * 100)
                        page.wait_for_timeout(4000)
                    except Exception:
                        print("-- Failed => More Comments --")

                page_counter = 1
                while True:
                    extract_and_print_comments(page, page_counter)
                    
                    next_button = page.locator("span.text-body2-strong").filter(has_text="بعدی").first
                    
                    if next_button.is_visible():
                        print(f"\n-- Go to page {page_counter + 1} --")
                        next_button.click(force=True)
                        
                        page_counter += 1
                        page.wait_for_timeout(4000)
                    else:
                        print("\n-- Scraping finished --")
                        break
            except Exception as url_error:
                print(f"Error URL: {url_error}")
                print("-- Move to the next URL --")
                continue

        browser.close()
