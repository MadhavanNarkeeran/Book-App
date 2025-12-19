import requests


class Book(object):
    def __init__(self, book_json):
        self.book_id = book_json["id"]
        self.title = book_json["volumeInfo"].get("title", "Unknown Title")
        self.authors = book_json["volumeInfo"].get("authors", [])
        self.publisher = book_json["volumeInfo"].get("publisher", "Unknown Publisher")
        self.publishedDate = book_json["volumeInfo"].get("publishedDate", "Unknown Published Date")
        self.description = book_json["volumeInfo"].get("description", "Unknown Description")
        self.pageCount = book_json["volumeInfo"].get("pageCount", 0)
        self.categories = book_json["volumeInfo"].get("categories", [])
        
        image_links = book_json["volumeInfo"].get("imageLinks", {})
        self.imageLink = image_links.get("medium") or image_links.get("thumbnail") or image_links.get("smallThumbnail") or ""

    def __repr__(self):
        return self.title


class BookClient(object):
    def __init__(self, api_key):
        self.sess = requests.Session()
        self.base_url = "https://www.googleapis.com/books/v1/volumes"
        self.api_key = api_key

    def search(self, search_string):
        params = {
            "q": search_string,
            "key": self.api_key,
            "startIndex": 0,
            "maxResults": 40,
            "projection": "full"
        }

        resp = self.sess.get(self.base_url, params=params)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()
        
        total_items = data.get("totalItems", 0)
        items_count = len(data.get("items", []))
        print(f"DEBUG: Total items available: {total_items}, Items returned in this request: {items_count}")

        result = []

        for book_json in data["items"]:
            result.append(Book(book_json))

        return result

    def retrieve_book_by_id(self, book_id):
        book_url = f"{self.base_url}/{book_id}"

        params = {
            "key": self.api_key,
            "projection": "full"
        }

        resp = self.sess.get(book_url, params=params)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed; make sure your API key is correct and authorized"
            )

        data = resp.json()

        book = Book(data)

        return book
