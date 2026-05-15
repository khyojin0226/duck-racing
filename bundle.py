import os
import base64
import re

# Paths
base_dir = r"C:\Users\T8G-2306-PC-001\.gemini\antigravity\playground\golden-copernicus"
input_html = os.path.join(base_dir, "index.html")
output_html = os.path.join(base_dir, "duck_race_standalone.html")

def get_base64_image(filename):
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"Warning: {filename} not found.")
        return ""
    with open(filepath, "rb") as f:
        data = f.read()
        return "data:image/png;base64," + base64.b64encode(data).decode('utf-8')

print("Reading index.html...")
with open(input_html, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Embed Background
print("Embedding background.png...")
bg_base64 = get_base64_image("background.png")
if bg_base64:
    content = content.replace("background.png", bg_base64)

# 2. Embed Ducks
print("Embedding duck images...")
duck_assets_js = "const DUCK_ASSETS = {\n"
for i in range(1, 26): # Check up to 25 just in case
    filename = f"duck{i}.png"
    if os.path.exists(os.path.join(base_dir, filename)):
        b64 = get_base64_image(filename)
        duck_assets_js += f"            {i}: '{b64}',\n"
duck_assets_js += "        };\n"

# Inject DUCK_ASSETS before Game Logic
content = content.replace("// --- 2. Game Logic ---", "// --- Asset Data ---\n" + duck_assets_js + "\n        // --- 2. Game Logic ---")

# 3. Replace Image Sources in JS
# Pattern 1: startRace initialization
# <img src="duck${p.duckId}.png"
# => <img src="${DUCK_ASSETS[p.duckId]}"
content = content.replace('src="duck${p.duckId}.png"', 'src="${DUCK_ASSETS[p.duckId]}"')

# Pattern 2: showResults
# Same replacement should work if the string is identical
# Let's verify if there are other variations.
# In showResults: <img src="duck${p.duckId}.png" ...
# It seems identical.

print("Writing standalone file...")
with open(output_html, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Success! Saved to {output_html}")
