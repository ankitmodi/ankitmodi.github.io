import os
import re
import shutil

SOURCE_DIR = 'past_blogs'
DEST_DIR = 'content/posts'

def migrate():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.md')]
    
    for filename in files:
        print(f"Migrating {filename}...")
        
        # Extract date from filename: YYYY-MM-DD-slug.md
        match = re.match(r'^(\d{4}-\d{1,2}-\d{1,2})-(.*)$', filename)
        date_str = None
        if match:
            date_str = match.group(1)
            # Normalize date to YYYY-MM-DD (e.g. 2020-3-19 -> 2020-03-19)
            # Not strictly necessary but good for sorting
            parts = date_str.split('-')
            date_str = f"{parts[0]}-{int(parts[1]):02d}-{int(parts[2]):02d}"
        
        src_path = os.path.join(SOURCE_DIR, filename)
        with open(src_path, 'r') as f:
            content = f.read()
            
        # Split FM and Body
        # Expecting file to start with ---
        parts = re.split(r'^---\s*$', content, flags=re.MULTILINE)
        
        if len(parts) < 3:
            print(f"Skipping {filename} - Invalid FM structure")
            continue
            
        fm_raw = parts[1]
        body_raw = parts[2:] # In case --- appears in body, we might need to be careful, but re.split usually does [empty, fm, body]
        body_raw = '---\n'.join(body_raw) # Rejoin if split accidentally, though usually body is just parts[2]
        
        # Process FM
        fm_lines = []
        has_date = False
        
        for line in fm_raw.strip().split('\n'):
            line = line.strip()
            if not line: continue
            
            if line.startswith('date:'):
                has_date = True
                
            fm_lines.append(line)
            
        if not has_date and date_str:
            fm_lines.append(f'date: {date_str}')
            
        # Ensure draft is false
        fm_lines.append('draft: false')
        
        # Reconstruct FM
        new_fm = '---\n' + '\n'.join(fm_lines) + '\n---\n'
        
        # Process Body
        
        # 1. Image Paths: {{ site.url }} -> ""
        body_raw = body_raw.replace('{{ site.url }}', '')
        
        # 2. Kramdown Images -> HTML
        def kramdown_sub(match):
            alt = match.group(1)
            src = match.group(2)
            attrs = match.group(3)
            src = src.replace('{{ site.url }}', '')
            # Simple conversion
            return f'<img src="{src}" alt="{alt}" {attrs}>'

        body_raw = re.sub(r'!\[(.*?)\]\((.*?)\)\{:\s*(.*?)\s*\}', kramdown_sub, body_raw)
        
        # 3. Goodreads Author Links formatting
        body_raw = re.sub(r'>_(.*?)_</a>', r'>\1</a>', body_raw)
        
        # 4. Rating Stars
        body_raw = body_raw.replace('___5 out of 5 stars___', '★★★★★')
        body_raw = body_raw.replace('___4 out of 5 stars___', '★★★★☆')
        body_raw = body_raw.replace('___3 out of 5 stars___', '★★★☆☆')
        body_raw = body_raw.replace('___2 out of 5 stars___', '★★☆☆☆')
        body_raw = body_raw.replace('___1 out of 5 stars___', '★☆☆☆☆')
        
        final_content = new_fm + body_raw
        
        # Write to dest
        dest_path = os.path.join(DEST_DIR, filename)
        with open(dest_path, 'w') as f:
            f.write(final_content)
            
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
