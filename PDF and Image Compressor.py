import subprocess
import os
from PIL import Image

GS_PATH = r"S:\GhostScript\gs10.07.0\bin\gswin64c.exe"

def compress_pdf(input_path, output_path, quality_choice):
    quality_map = {
        "1": "/screen",   # 72 DPI
        "2": "/ebook",    # 150 DPI
        "3": "/printer",  # 300 DPI
        "4": "/prepress"  # Max Quality
    }
    setting = quality_map.get(quality_choice, "/ebook")
    
    args = [
        GS_PATH, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={setting}', '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_path}', input_path
    ]
    
    subprocess.run(args, check=True)

def compress_image(input_path, output_path, quality_choice):
    # Mapping 1-4 menu choices to Pillow 0-100 quality scale
    quality_map = {"1": 30, "2": 60, "3": 85, "4": 95}
    q_value = quality_map.get(quality_choice, 75)
    
    with Image.open(input_path) as img:
        # Convert to RGB if it's a PNG/RGBA to ensure JPEG compatibility
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        img.save(output_path, "JPEG", quality=q_value, optimize=True)

def main():
    print("\nPDF & Image Compressor")
    
    file_path = input("Enter the full path of the file: ").strip().replace('"', '')
    
    if not os.path.exists(file_path):
        print("Error: File not found. Please check the path and try again.")
        return

    ext = os.path.splitext(file_path)[1].lower()
    
    print("\nSelect Quality Level:")
    print("1. [Low]    - Smallest file size")
    print("2. [Medium] - Balanced (Recommended)")
    print("3. [High]   - Great for printing")
    print("4. [Max]    - Almost no loss")
    
    choice = input("\nEnter choice (1-4): ")

    # Output path name
    dir_name = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    if ext == ".pdf":
        output_path = os.path.join(dir_name, f"{base_name}_compressed.pdf")
        compress_pdf(file_path, output_path, choice)
    elif ext in [".jpg", ".jpeg", ".png", ".webp"]:
        output_path = os.path.join(dir_name, f"{base_name}_compressed.jpg")
        compress_image(file_path, output_path, choice)
    else:
        print(f"Unsupported file type: {ext}")
        return

    # Results
    old_size = os.path.getsize(file_path) / 1024
    new_size = os.path.getsize(output_path) / 1024
    print(f"\nDone! \nOriginal: {old_size:.1f}KB \nCompressed: {new_size:.1f}KB")

if __name__ == "__main__":
    main()