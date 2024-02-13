from PIL import Image
from PIL.ExifTags import TAGS

def analyze_image_metadata(image_path):
    try:

        with Image.open(image_path) as img:

            metadata = img.info
            exif_data = img._getexif()


            print("Image Metadata:")
            print("---------------")
            for tag, value in metadata.items():
                print(f"{tag}: {value}")

            if exif_data is not None:
                print("\nEXIF Data:")
                print("----------")
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    print(f"{tag_name}: {value}")

    except Exception as e:
        print(f"Error analyzing image metadata: {e}")

if __name__ == "__main__":

    image_path = 'your_image_path.jpg'
    analyze_image_metadata(image_path)
