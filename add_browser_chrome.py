import os
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
    tab_w = 230
    tab_x0, tab_y0, tab_x1, tab_y1 = 8, 8, 8 + tab_w, 42
    draw.rounded_rectangle([tab_x0, tab_y0, tab_x1, tab_y1], radius=8, fill=(255, 255, 255, 255))
    # Fill bottom corners so it connects seamlessly to the toolbar
    draw.rectangle([tab_x0, 34, tab_x1, 42], fill=(255, 255, 255, 255))
    
    # Window controls (top right)
    # Minimize, Maximize, Close
    ctrl_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    draw.text((W - 130, 10), "—", font=ctrl_font, fill=(90, 90, 90, 255))
    draw.text((W - 85, 10), "▢", font=ctrl_font, fill=(90, 90, 90, 255))
    draw.text((W - 40, 10), "✕", font=ctrl_font, fill=(90, 90, 90, 255))
    
    # Fonts
    font_tab = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    font_url = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    font_icon = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
    
    # Tab content
    # Favicon circle
    draw.ellipse([tab_x0 + 12, tab_y0 + 9, tab_x0 + 24, tab_y0 + 21], fill=(26, 115, 232, 255))
    # Tab title (truncate if needed)
    display_title = tab_title if len(tab_title) < 25 else tab_title[:22] + "..."
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
    omni_y0 = 48
    omni_x1 = W - 100
    omni_y1 = 76
    draw.rounded_rectangle([omni_x0, omni_y0, omni_x1, omni_y1], radius=14, fill=(241, 243, 244, 255))
    
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
    print(f"Saved {output_path}")

if __name__ == "__main__":
    create_browser_image(
        r"C:\xampp\htdocs\Best Car Dealership\dealersbystate.png",
        r"C:\xampp\htdocs\Best Car Dealership\test_dealersbystate.png",
        "http://127.0.0.1:8000/dealers/",
        "Dealerships"
    )
