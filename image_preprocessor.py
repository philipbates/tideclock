import io
import time
import urllib.request
from PIL import Image, ImageOps

def crop_and_convert_4gray(img, target_width=800, target_height=480):
    """
    Crops the image to a target aspect ratio (800x480 center-crop),
    converts it to grayscale, and quantizes it to exactly 4 distinct shades.
    """
    print("Resizing and cropping image to match the screen aspect ratio...")
    
    # 1. Use ImageOps.fit to perform a high-quality center crop and resize
    img_cropped = ImageOps.fit(img, (target_width, target_height), Image.Resampling.LANCZOS)
    
    # 2. Convert to standard 8-bit Grayscale (PIL "L" mode)
    img_gray = img_cropped.convert("L")
    
    # 3. Downsample to exactly 4 grayscale shades (0, 85, 170, 255)
    # This prevents the driver from struggling with intermediate shades.
    print("Quantizing to 4 levels of grayscale...")
    img_4gray = img_gray.point(lambda x: int(x / 64) * 85)
    
    return img_4gray

if __name__ == "__main__":
    # Example URL (high-contrast portrait image)
    TARGET_image = "wave.jpg"
    
    try:
        # Step 1: Get the image
        raw_image = Image.open(TARGET_image)
        
        # Step 2: Prep it for the EPD (800x480, 4 shades of Gray)
        final_image = crop_and_convert_4gray(raw_image, target_width=800, target_height=480)
        
        # (Optional) Save locally to verify the visual conversion first
        final_image.save("prepped_for_epd.png")
        print("Prepped image saved locally as 'prepped_for_epd.png'")
        

        
    except Exception as e:
        print(f"An error occurred: {e}")