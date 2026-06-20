import httpx
from bs4 import BeautifulSoup

def preview_page(url: str):
    print(f"fetching:{url}.....\n")

    try:

        response = httpx.get(url, follow_redirects=True)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        
        print(f"page title : { soup.title.string if soup.title else "No title found"}")

        print("page content")
        text_content = soup.get_text(separator="\n", strip=True)
        print(text_content)

        print("Discovered links:\n")

        for index, a in enumerate(soup.find_all("a", href = True), 1):
            link_text = a.get_text(strip=True) or "[no text]"
            link_href = a["href"]
            print(f"[{index}] {link_text} -> ({link_href})")

    except Exception as e:
        print(f"Error fetching the page: {e}")

def main():
    target = input("Enter the url: ")
    preview_page(target)

if __name__ == "__main__":
    main()
