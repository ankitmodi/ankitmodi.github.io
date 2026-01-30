import os
import re
import urllib.request
import subprocess
import glob
import argparse
import shutil

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

def process_year(year):
    print(f"Processing year {year}...")
    
    # Find the file
    files = glob.glob(os.path.join(CONTENT_DIR, f"*{year}.md"))
    if not files:
        print(f"No file found for year {year}")
        return
    
    if len(files) > 1:
        # filter for 'my-year-in-books'
        files = [f for f in files if 'my-year-in-books' in f]
    
    if not files:
         print(f"No specific book post found for year {year}")
         return

    target_file = files[0]
    print(f"Target file: {target_file}")
    
    with open(target_file, 'r') as f:
        content = f.read()
        
    # Extract book images
    # Pattern to match: <img src="URL" ...>
    # We want to capture the URL.
    # Note: the file uses single ' or double " quotes. 
    img_pattern = re.compile(r'<img src=["\'](https://.*?goodreads\.com.*?)["\']', re.IGNORECASE)
    matches = img_pattern.findall(content)
    
    print(f"Found {len(matches)} book images.")
    
    if not matches:
        print("No goodreads images found.")
        return

    # Setup directories
    year_assets_dir = os.path.join(STATIC_ASSETS_DIR, f"{year}_books")
    if not os.path.exists(year_assets_dir):
        os.makedirs(year_assets_dir)
        
    temp_dir = f"temp_books_{year}"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    local_images_map = {} # url -> new_local_path (for markdown replacement)
    downloaded_files_for_collage = []

    for i, url in enumerate(matches):
        ext = url.split('.')[-1]
        if len(ext) > 4 or '/' in ext: ext = 'jpg'
        
        # Naming: 01.jpg, 02.jpg
        filename = f"{i+1:02d}.{ext}"
        filepath_static = os.path.join(year_assets_dir, filename)
        filepath_temp = os.path.join(temp_dir, filename)
        
        # Download (if not exists or overwrite? Let's overwrite to ensure we have them)
        if not os.path.exists(filepath_static):
            print(f"Downloading {i+1}/{len(matches)}: {url}")
            if download_image(url, filepath_static):
                pass
            else:
                continue
        else:
            print(f"Skipping download for {filename}, already exists.")
        
        # Copy to temp for collage with consistent filenames
        shutil.copy(filepath_static, filepath_temp)
        downloaded_files_for_collage.append(filepath_temp)
        
        # Map for markdown update: /assets/images/2019_books/01.jpg
        local_web_path = f"/assets/images/{year}_books/{filename}"
        local_images_map[url] = local_web_path

    # Generate Collage
    collage_filename = f"{year}_overview.png"
    collage_output_path = os.path.join(year_assets_dir, collage_filename)
    
    print("Generating collage...")
    cmd = [
        "montage",
        os.path.join(temp_dir, "*"),
        "-geometry", "x300+10+10",
        "-tile", "4x", # Max 4 per row
        "-background", "white",
        collage_output_path
    ]
    
    try:
        subprocess.check_call(cmd)
        print(f"Collage created at {collage_output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Montage failed: {e}")
        # Continue anyway to update links? No, maybe collage is important. But let's continue.

    # Cleanup temp
    shutil.rmtree(temp_dir)
    
    # Update Markdown
    new_content = content
    
    # 1. Replace URLs
    for url, local_path in local_images_map.items():
        new_content = new_content.replace(url, local_path)
        
    # 2. Add Collage at the top
    # Look for the first header or introduction.
    # In 2021 post, it was inserted before the first book.
    # In these files, there is an intro text, then `### 1. ...`
    # We can insert it after the front matter and before the first `###`.
    
    collage_html = f'\n<img src="/assets/images/{year}_books/{collage_filename}" alt="{year} Books Overview" style="width: 100%; height: auto; display: block; margin: 1rem 0;">\n\n'
    
    # Check if collage already exists (to avoid duplicates)
    if collage_filename not in new_content:
        # Find position to insert
        # We try to find the start of the list.
        # usually ends of front matter `---`
        parts = new_content.split('---')
        if len(parts) >= 3:
            # parts[0] is empty, parts[1] is frontmatter, parts[2] is body.
            # We want to insert after the first paragraph of body? 
            # Or just after frontmatter?
            # User might want it after the intro text "Here are the books..."
            # Let's look for "Here are the books" or similar text.
            # Or insert before the first `###`.
            
            first_h3_index = new_content.find('###')
            if first_h3_index != -1:
                # Insert before the first ###
                new_content = new_content[:first_h3_index] + collage_html + new_content[first_h3_index:]
            else:
                # Append if no H3
                new_content = new_content + collage_html
        else:
            print("Could not parse frontmatter, checking manual insertion.")
            
    with open(target_file, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {target_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=str, required=True, help="Year to process (2019 or 2020)")
    args = parser.parse_args()
    
    process_year(args.year)
