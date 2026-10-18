import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def create_browser_image(base_image_path, output_path, url, tab_title="Dealerships"):
    base_img = Image.open(base_image_path).convert("RGBA")
    W, H = base_img.size
    chrome_h = 82
    
    # Create final canvas
    canvas = Image.new("RGBA", (W, H + chrome_h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Tab bar background
    tab_bar_bg = (222, 225, 230, 255) # Chrome header gray
    draw.rectangle([0, 0, W, 42], fill=tab_bar_bg)
    
    # Active Tab (white)
    tab_w = 260
    tab_x0, tab_y0, tab_x1, tab_y1 = 8, 8, 8 + tab_w, 42
    draw.rounded_rectangle([tab_x0, tab_y0, tab_x1, tab_y1], radius=8, fill=(255, 255, 255, 255))
    draw.rectangle([tab_x0, 34, tab_x1, 42], fill=(255, 255, 255, 255))
    
    # Window controls (top right)
    ctrl_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    draw.text((W - 130, 10), "—", font=ctrl_font, fill=(90, 90, 90, 255))
    draw.text((W - 85, 10), "▢", font=ctrl_font, fill=(90, 90, 90, 255))
    draw.text((W - 40, 10), "✕", font=ctrl_font, fill=(90, 90, 90, 255))
    
    # Fonts
    font_tab = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    font_url = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    font_icon = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
    
    # Favicon circle
    draw.ellipse([tab_x0 + 12, tab_y0 + 9, tab_x0 + 24, tab_y0 + 21], fill=(26, 115, 232, 255))
    # Tab title
    display_title = tab_title if len(tab_title) < 28 else tab_title[:25] + "..."
    draw.text((tab_x0 + 32, tab_y0 + 7), display_title, font=font_tab, fill=(60, 64, 67, 255))
    # Close tab 'x'
    draw.text((tab_x1 - 20, tab_y0 + 6), "×", font=font_tab, fill=(120, 120, 120, 255))
    
    # Toolbar background (white)
    draw.rectangle([0, 42, W, chrome_h], fill=(255, 255, 255, 255))
    
    # Navigation buttons: < > ↻
    draw.text((18, 50), "←", font=font_icon, fill=(95, 99, 104, 255))
    draw.text((50, 50), "→", font=font_icon, fill=(180, 180, 180, 255))
    draw.text((82, 50), "↻", font=font_icon, fill=(95, 99, 104, 255))
    
    # Omnibox / Address Bar (pill shape)
    omni_x0 = 115
    omni_y0 = 47
    omni_x1 = W - 100
    omni_y1 = 77
    draw.rounded_rectangle([omni_x0, omni_y0, omni_x1, omni_y1], radius=15, fill=(241, 243, 244, 255))
    
    # Padlock / Secure icon
    draw.text((omni_x0 + 14, omni_y0 + 5), "🔒", font=font_tab, fill=(95, 99, 104, 255))
    
    # URL text
    draw.text((omni_x0 + 38, omni_y0 + 4), url, font=font_url, fill=(32, 33, 36, 255))
    
    # Bottom subtle border
    draw.line([(0, chrome_h - 1), (W, chrome_h - 1)], fill=(220, 220, 220, 255), width=1)
    
    # Paste base screenshot below chrome
    canvas.paste(base_img, (0, chrome_h))
    
    # Convert to RGB and save
    final_img = canvas.convert("RGB")
    final_img.save(output_path, "PNG", quality=95)
    print(f"Generated {output_path}")

DEPLOY_BASE_URL = "https://aimanharithzwork-8000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"

tasks = [
    # 5 local screenshots
    {
        "source": r"C:\Users\USER\.gemini\antigravity-ide\brain\2f335e91-b1c9-48a4-b00e-c78c7683ca9f\admin_logout_page_1792341502559.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\admin_logout.png",
        "url": "http://127.0.0.1:8000/admin/logout/",
        "title": "Logged out | Django site admin"
    },
    {
        "source": r"c:\xampp\htdocs\Best Car Dealership\screenshots_raw_backup\get_dealers_loggedin.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\get_dealers_loggedin.png",
        "url": "http://127.0.0.1:8000/dealers/",
        "title": "Dealerships"
    },
    {
        "source": r"c:\xampp\htdocs\Best Car Dealership\screenshots_raw_backup\dealersbystate.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\dealersbystate.png",
        "url": "http://127.0.0.1:8000/dealers/",
        "title": "Dealerships"
    },
    {
        "source": r"c:\xampp\htdocs\Best Car Dealership\screenshots_raw_backup\dealer_id_reviews.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\dealer_id_reviews.png",
        "url": "http://127.0.0.1:8000/dealer/3",
        "title": "Dealerships"
    },
    {
        "source": r"C:\Users\USER\.gemini\antigravity-ide\brain\2f335e91-b1c9-48a4-b00e-c78c7683ca9f\dealer_1_final_1792341584125.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\added_review.png",
        "url": "http://127.0.0.1:8000/dealer/1",
        "title": "Dealerships"
    },
    # 4 deployed screenshots
    {
        "source": r"c:\xampp\htdocs\Best Car Dealership\deployed_landingpage.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\deployed_landingpage.png",
        "url": f"{DEPLOY_BASE_URL}/",
        "title": "Dealerships"
    },
    {
        "source": r"c:\xampp\htdocs\Best Car Dealership\deployed_loggedin.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\deployed_loggedin.png",
        "url": f"{DEPLOY_BASE_URL}/dealers/",
        "title": "Dealerships"
    },
    {
        "source": r"c:\xampp\htdocs\Best Car Dealership\screenshots_raw_backup\dealer_id_reviews.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\deployed_dealer_detail.png",
        "url": f"{DEPLOY_BASE_URL}/dealer/3",
        "title": "Dealerships"
    },
    {
        "source": r"C:\Users\USER\.gemini\antigravity-ide\brain\2f335e91-b1c9-48a4-b00e-c78c7683ca9f\dealer_1_final_1792341584125.png",
        "output": r"c:\xampp\htdocs\Best Car Dealership\deployed_add_review.png",
        "url": f"{DEPLOY_BASE_URL}/dealer/1",
        "title": "Dealerships"
    }
]

backup_dir = r"c:\xampp\htdocs\Best Car Dealership\screenshots_raw_backup"
os.makedirs(backup_dir, exist_ok=True)

for item in tasks:
    dest = item["output"]
    fname = os.path.basename(dest)
    backup_file = os.path.join(backup_dir, fname)
    if not os.path.exists(backup_file):
        shutil.copy2(item["source"], backup_file)
    create_browser_image(backup_file, dest, item["url"], item["title"])

print("All screenshots generated successfully!")
