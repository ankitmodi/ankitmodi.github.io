import os
import urllib.request
import subprocess

# List of image URLs extracted from the blog post
IMAGE_URLS = [
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1430942575l/22609391.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1423763749l/6900.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1474169725l/15881.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1474154022l/3.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1554006152l/6.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1637581438l/12007777.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1581527774l/41881472.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1432531998l/25596931.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1358746649l/154126.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1630547330l/5.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1479724111l/23265596.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1320528453l/4948826.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1510351877l/35749414.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1347627171l/463484.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1570034350l/12840933.jpg",
    "https://s.gr-assets.com/assets/nophoto/book/50x75-a91bf249278a81aabab721ef782c4a74.png", 
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1339395245l/4887.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1379237941l/11801713.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1347378709l/830364.jpg",
    "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1333577589l/8694.jpg"
]

TEMP_DIR = "temp_books_2021"
OUTPUT_PATH = "static/assets/images/2021_books/2021_overview.png"

def create_collage():
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        
    print(f"Downloading {len(IMAGE_URLS)} images...")
    
    downloaded_files = []
    
    for i, url in enumerate(IMAGE_URLS):
        try:
            # We preserve sequence in filename so montage orders them correctly
            # 01.jpg, 02.jpg ...
            ext = url.split('.')[-1]
            if len(ext) > 4 or '/' in ext: ext = 'jpg'
            
            filename = f"{i:02d}.{ext}"
            filepath = os.path.join(TEMP_DIR, filename)
            
            # Download with User-Agent to avoid some blocking
            req = urllib.request.Request(
                url, 
                data=None, 
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            
            with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
                
            downloaded_files.append(filepath)
            
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    if not downloaded_files:
        print("No images downloaded.")
        return

    print("Running montage...")
    # Montage command
    # -geometry x400 : fixed height 400, width auto (to preserve aspect ratio)
    # Actually, montage -geometry usually sets max bounding box. 
    # If we want uniform height and packed, it's tricky with simple geometry.
    # But -geometry x300 is usually good enough.
    # -tile 5x : 5 columns
    # -background white
    # -shadow? -border?
    
    cmd = [
        "montage",
        os.path.join(TEMP_DIR, "*"),
        "-geometry", "x300+10+10", # Height 300, spacing 10
        "-tile", "4x",
        "-background", "white",
        OUTPUT_PATH
    ]
    
    try:
        subprocess.check_call(cmd)
        print(f"Collage saved to {OUTPUT_PATH}")
    except subprocess.CalledProcessError as e:
        print(f"Montage failed: {e}")
        
    # Cleanup (optional, keeping for debug for now)
    # shutil.rmtree(TEMP_DIR)


if __name__ == "__main__":
    create_collage()
