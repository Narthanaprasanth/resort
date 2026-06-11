import re

html_file = r"c:\Users\HP\Downloads\Resort_Agent_Portal_MASTER_TEMPLATE (2) - Copy\Resort_Agent_Portal_MASTER_TEMPLATE (3).html"
css_file = r"c:\Users\HP\Downloads\Resort_Agent_Portal_MASTER_TEMPLATE (2) - Copy\frontend\src\index.css"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract config
config_match = re.search(r'<script>\s*const CONFIG = (.*?);\s*</script>', content, re.DOTALL)
config_json = config_match.group(1)

with open(r"c:\Users\HP\Downloads\Resort_Agent_Portal_MASTER_TEMPLATE (2) - Copy\frontend\src\config.js", 'w', encoding='utf-8') as f:
    f.write(f"export const CONFIG = {config_json};\n")

# Extract CSS
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    css_content = style_match.group(1)
    
    # We will prepend google fonts import
    fonts_import = "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');\n\n"
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(fonts_import + css_content)
        
print("Extraction successful.")
