import sys
import os
from PIL import Image
from PIL.ExifTags import TAGS
from geopy.geocoders import Nominatim

def convert_gps_coordinates(gps_info):
    latitude = gps_info[2][0] + gps_info[2][1] / 60 + gps_info[2][2] / 3600
    longitude = gps_info[4][0] + gps_info[4][1] / 60 + gps_info[4][2] / 3600

    if gps_info[1] == 'S':
        latitude = -latitude

    if gps_info[3] == 'W':
        longitude = -longitude

    return latitude, longitude

def reverse_geocode(coordinates):
    geolocator = Nominatim(user_agent="image-metadata-tool")
    try:
        location = geolocator.reverse(coordinates, language="en", exactly_one=True)
        if location and location.address:
            return location.address
        else:
            return "Location information not available."
    except Exception as e:
        print(f"Error during reverse geocoding: {e}")
        return "Error during reverse geocoding."

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

                # Check for GPSInfo tag (34853)
                if 34853 in exif_data:
                    gps_info = exif_data[34853]
                    print("\nGPS Info:")
                    print("---------")
                    for tag, value in gps_info.items():
                        tag_name = TAGS.get(tag, tag)
                        print(f"{tag_name}: {value}")

                    # Convert GPS coordinates to decimal degrees
                    if 2 in gps_info and 4 in gps_info:
                        converted_coordinates = convert_gps_coordinates(gps_info)
                        print("\nConverted Coordinates:")
                        print(f"Latitude: {converted_coordinates[0]}")
                        print(f"Longitude: {converted_coordinates[1]}")

                        # Reverse geocoding
                        coordinates = (converted_coordinates[0], converted_coordinates[1])
                        location_info = reverse_geocode(coordinates)
                        print("\nLocation Information:")
                        print(location_info)
                    else:
                        print("Latitude and/or Longitude information not available.")
                else:
                    print("No GPS Info found.")
            else:
                print("No EXIF data found in the image.")

    except Exception as e:
        print(f"Error analyzing image metadata: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.isfile(image_path):
        print(f"Error: File not found - {image_path}")
        sys.exit(1)

    analyze_image_metadata(image_path)
