import urllib.request
import os

images = [
    ("https://basecamp.com/assets/books/shapeup/3.2/back-end_only-e8b9580807d4b4b50a31627b20d37c1dcf90c55b1f0cc20d5ab88f25888b6bf6.png", "static/assets/images/shapeup/back-end_only.png"),
    ("https://basecamp.com/assets/books/shapeup/3.2/one_slice-4cbcdda1a5cdc1b2bdc9bf7bd023cc0c5af666c5857c6e7d32650d9229a81cf0.png", "static/assets/images/shapeup/one_slice.png"),
    ("https://basecamp.com/assets/books/shapeup/3.3/drafts_6-a511456472dd9b348e6fc314781a8e6c91e7ae942eed0779036539bf27bbb530.png", "static/assets/images/shapeup/drafts_6.png"),
    ("https://basecamp.com/assets/books/shapeup/3.4/snapshots-acc8efc1f87284428ed51816961e7f6f40141ff29cf1103c3d0002e73b0da497.png", "static/assets/images/shapeup/snapshots.png"),
    ("https://basecamp.com/assets/books/shapeup/3.5/compare_to_baseline-ff521686dc8ea60cb9587d072409f5ee8bba79ca269e0fb04963b930699fb62d.jpg", "static/assets/images/shapeup/compare_to_baseline.jpg")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Referer": "https://basecamp.com/"
}

for url, path in images:
    print(f"Downloading {url} to {path}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
             with open(path, 'wb') as f:
                f.write(response.read())
        print("Success!")
    except Exception as e:
        print(f"Failed: {e}")
