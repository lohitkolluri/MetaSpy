import sys
from PIL import Image
from PIL.ExifTags import TAGS

def analyze_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()

            if exif_data is not None:
                print("EXIF Data:")
                print("----------")
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    print(f"{tag_name}: {value}")
            else:
                print("No EXIF data found in the image.")

    except Exception as e:
        print(f"Error analyzing image metadata: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    analyze_image_metadata(image_path)
