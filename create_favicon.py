#!/usr/bin/env python3
"""
Script to create a custom favicon for the Matrix Eigenvalue Visualizer
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_favicon():
    # Create a 32x32 image (will be scaled down to 16x16 for favicon)
    size = (32, 32)
    image = Image.new('RGBA', size, (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    
    # Define colors based on the app's theme
    bg_color = (26, 26, 46)  # --bg-secondary from CSS
    accent_color = (94, 155, 255)  # --accent-secondary from CSS
    text_color = (100, 255, 218)  # --accent-primary from CSS
    
    # Draw a rounded rectangle background
    draw.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=8, fill=bg_color)
    
    # Draw a matrix-like pattern
    cell_size = 6
    start_x, start_y = 6, 6
    
    # Draw grid lines
    for i in range(3):
        for j in range(3):
            x = start_x + i * cell_size
            y = start_y + j * cell_size
            draw.rectangle([x, y, x + cell_size - 2, y + cell_size - 2], fill=accent_color)
    
    # Draw an eigenvalue symbol (lambda)
    try:
        # Try to use a font if available
        font = ImageFont.truetype("DejaVuSans.ttf", 12)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw a lambda symbol or 'λ' to represent eigenvalues
    draw.text((18, 8), "λ", fill=text_color, font=font)
    
    # Resize to 16x16 for the final favicon
    favicon = image.resize((16, 16), Image.Resampling.LANCZOS)
    
    # Save as favicon.ico
    favicon.save('/workspace/static/favicon.ico', format='ICO')
    
    print("Custom favicon created successfully!")
    
    # Also save a larger version for high-resolution displays
    image.save('/workspace/static/favicon-32x32.png', format='PNG')

if __name__ == "__main__":
    create_favicon()