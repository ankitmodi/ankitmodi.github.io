import os
import re
import urllib.request
import subprocess
import shutil
import argparse
from datetime import datetime

# Dependency check
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup not found. Please install it: pip install beautifulsoup4")
    exit(1)

BASE_DIR = os.path.abspath(".")
CONTENT_DIR = os.path.join(BASE_DIR, "content/posts")
STATIC_ASSETS_DIR = os.path.join(BASE_DIR, "static/assets/images")

def download_image(url, filepath):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def clean_cover_url(url):
    # Remove sizing info like ._SY75_ or ._SX50_
    # Example: .../30658._SY75_.jpg -> .../30658.jpg
    # Also handles _SY475_ or similar
    return re.sub(r'\._S[XY]\d+_', '', url)

def main():
    parser = argparse.ArgumentParser(description="Scrape Goodreads 'Read' shelf from HTML export")
    parser.add_argument("--file", default="read_source.html", help="Path to the saved Goodreads HTML file")
    parser.add_argument("--year", default="2025", help="Year to filter books by")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Date for the blog post (YYYY-MM-DD)")
    args = parser.parse_args()

    source_file = args.file
    year = args.year
    post_date_str = args.date
    
    if not os.path.exists(source_file):
        print(f"File {source_file} not found! Please save your Goodreads 'Read' shelf page (with infinite scroll loaded) as HTML.")
        return

    print(f"Parsing {source_file}...")
    with open(source_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    books = []
    
    # Select rows with class 'bookalike review'
    rows = soup.select('tr.bookalike.review')
    print(f"Found {len(rows)} books in the file.")

    for row in rows:
        # Date Read
        date_read_span = row.select_one('.date_read_value')
        if not date_read_span:
            continue
        
        date_read_text = date_read_span.get_text(strip=True)
        if year not in date_read_text:
            continue

        # Extract Details
        title_tag = row.select_one('.field.title a')
        title = title_tag.get_text(strip=True)
        # Handle cases where title might be truncated (title attribute usually full)
        if title_tag.get('title'):
            title = title_tag['title']
            
        book_link = "https://www.goodreads.com" + title_tag['href']
        
        author_tag = row.select_one('.field.author a')
        author = author_tag.get_text(strip=True)
        
        # Rating
        stars_div = row.select_one('.stars')
        rating = 0
        if stars_div and stars_div.has_attr('data-rating'):
            rating = int(stars_div['data-rating'])
            
        # Cover
        cover_img = row.select_one('.field.cover img')
        cover_url = ""
        if cover_img:
            cover_url = clean_cover_url(cover_img['src'])
            
        # Review
        # Try hidden full text first (Goodreads often hides full review in a span)
        review_full = row.select_one('span[id^="freeTextreview"][style*="display:none"]')
        review_text = ""
        if review_full:
            review_text = review_full.decode_contents() 
        else:
            # Try visible text if full text not hidden
            review_short = row.select_one('span[id^="freeTextContainerreview"]')
            if review_short:
                review_text = review_short.decode_contents()

        books.append({
            'title': title,
            'author': author,
            'rating': rating,
            'cover_url': cover_url,
            'review': review_text,
            'book_link': book_link,
            'date_read': date_read_text
        })

    print(f"Found {len(books)} books read in {year}.")
    
    if not books:
        print("No books found. Check the year or the HTML file.")
        return

    # Sort by rating (descending)
    books.sort(key=lambda x: x['rating'], reverse=True)

    # Setup directories
    year_assets_dir = os.path.join(STATIC_ASSETS_DIR, f"{year}_books")
    if not os.path.exists(year_assets_dir):
        os.makedirs(year_assets_dir)
        
    temp_dir = f"temp_books_{year}"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Download images
    downloaded_files_for_collage = []
    
    for i, book in enumerate(books):
        ext = book['cover_url'].split('.')[-1]
        if len(ext) > 4: ext = 'jpg' # Default extension if weird
        
        filename = f"{i+1:02d}.{ext}"
        filepath_static = os.path.join(year_assets_dir, filename)
        filepath_temp = os.path.join(temp_dir, filename) 
        
        print(f"Downloading {i+1}/{len(books)}: {book['title']}")
        if not os.path.exists(filepath_static):
            download_image(book['cover_url'], filepath_static)
        
        shutil.copy(filepath_static, filepath_temp)
        downloaded_files_for_collage.append(filepath_temp)
        
        book['local_image_path'] = f"/assets/images/{year}_books/{filename}"

    # Generate Collage
    collage_filename = f"{year}_overview.png"
    collage_output_path = os.path.join(year_assets_dir, collage_filename)
    
    print("Generating collage...")
    # Check if montage exists
    if shutil.which("montage"):
        try:
            # -geometry x300 -> 300px height, width auto
            cmd = [
                "montage",
                os.path.join(temp_dir, "*"),
                "-geometry", "x300+10+10",
                "-tile", "4x",
                "-background", "white",
                collage_output_path
            ]
            subprocess.check_call(cmd)
            print(f"Collage created at {collage_output_path}")
        except subprocess.CalledProcessError:
            print("Montage command failed.")
            collage_output_path = None
    else:
        print("Montage command (ImageMagick) not found. Skipping collage generation.")
        collage_output_path = None

    # Cleanup temp
    shutil.rmtree(temp_dir)

    # Generate Markdown
    md_output_path = os.path.join(CONTENT_DIR, f"{post_date_str}-my-year-in-books-{year}.md")
    
    with open(md_output_path, 'w', encoding='utf-8') as f:
        # Frontmatter
        f.write("---\n")
        f.write("layout: post\n")
        f.write(f"title: My Year in Books - {year}\n")
        f.write(f"excerpt: Here's what I read in {year} - in order of what I liked most.\n")
        if collage_output_path:
            f.write("image:\n")
            f.write(f'  path: "{{{{ site.url }}}}/assets/images/{year}_books/{collage_filename}"\n')
        f.write(f"date: {post_date_str}\n")
        f.write("draft: false\n")
        f.write("---\n\n")
        
        if collage_output_path:
            f.write(f"![cover image](/assets/images/{year}_books/{collage_filename})\n\n")
            
        f.write(f"Here's what I read in {year} - in order of what I liked most (highest rated first):\n\n")
        
        for i, book in enumerate(books):
            rank = i + 1
            rating_stars = "★" * book['rating'] + "☆" * (5 - book['rating'])
            
            f.write(f"### <a href='{book['book_link']}' target='_blank'>{rank}. {book['title']}</a>\n")
            f.write(f"<img src=\"{book['local_image_path']}\" alt=\"cover image\" height='300' width='200px' style='float:left; padding-right:20px; padding-bottom:5px; padding-top:5px'>\n")
            f.write(f"Author: {book['author']}\n")
            f.write("<br>\n")
            f.write(f"My rating: {rating_stars}\n")
            f.write("<br><br>\n")
            f.write(f"{book['review']}\n")
            f.write("<br clear=\"all\"><br>\n\n\n\n")

    print(f"Successfully created {md_output_path}")

if __name__ == "__main__":
    main()
