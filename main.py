import os
import shutil
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(script_dir, "entry.png")
    
    if not os.path.exists(src):
        print(f"Error: Source image {src} not found. Please run draw.py first.", file=sys.stderr)
        sys.exit(1)
        
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        print(f"Error: Failed to create output directory {output_dir}: {e}", file=sys.stderr)
        sys.exit(1)
        
    dst = os.path.join(output_dir, "entry.png")
    try:
        shutil.copyfile(src, dst)
        print(f"Successfully copied entry.png to {dst}")
    except Exception as e:
        print(f"Error: Failed to copy entry.png to {dst}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
