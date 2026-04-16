import os
import re
import shutil

def main():
    base_dir = r"c:\Users\HOME\Documents\site novo Rosiane"
    index_path = os.path.join(base_dir, "index.html")
    
    css_dir = os.path.join(base_dir, "assets", "css")
    js_dir = os.path.join(base_dir, "assets", "js")
    img_dir = os.path.join(base_dir, "assets", "images")
    
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Extract CSS
    style_start = content.find("<style>")
    style_end = content.find("</style>")
    
    if style_start != -1 and style_end != -1:
        css_content = content[style_start + len("<style>"):style_end]
        
        # Write to file
        with open(os.path.join(css_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write(css_content.strip() + "\n")
            
        # Replace in HTML
        html_before_style = content[:style_start]
        html_after_style = content[style_end + len("</style>"):]
        content = html_before_style + '<link rel="stylesheet" href="assets/css/style.css" />\n' + html_after_style

    # 2. Extract JS
    script_start = content.rfind("<script>")
    script_end = content.rfind("</script>")
    
    if script_start != -1 and script_end != -1 and script_start > content.rfind("</footer>"):
        js_content = content[script_start + len("<script>"):script_end]
        
        # Write JS to file
        with open(os.path.join(js_dir, "main.js"), "w", encoding="utf-8") as f:
            f.write(js_content.strip() + "\n")
            
        # Replace in HTML
        html_before_js = content[:script_start]
        html_after_js = content[script_end + len("</script>"):]
        content = html_before_js + '<script src="assets/js/main.js" defer></script>\n' + html_after_js

    # 3. Process Images
    # find images `<img ... src="..." ...>`
    # We will search for src="..." where extension is image.
    pattern = r'src="([^"]+\.(?:png|jpg|jpeg|webp|gif|svg))"'
    
    def replacer(match):
        orig_src = match.group(1)
        # Skip if it's already in assets/images or external URL
        if orig_src.startswith("assets/images/") or orig_src.startswith("http"):
            return match.group(0)
            
        filename = os.path.basename(orig_src)
        new_src = f"assets/images/{filename}"
        
        # Copy file
        # The src might be relative to base_dir
        source_path = os.path.join(base_dir, orig_src.replace('/', os.sep))
        dest_path = os.path.join(img_dir, filename)
        
        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, dest_path)
                print(f"Copied: {source_path} -> {dest_path}")
            except Exception as e:
                print(f"Error copying {source_path}: {e}")
        else:
            print(f"Warning: Source image not found - {source_path}")
            
        return f'src="{new_src}"'

    content = re.sub(pattern, replacer, content)

    # 4. Save new index.html
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Refactoring complete.")

if __name__ == "__main__":
    main()
