
import requests
import os
from PIL import Image

def test_upload_valid():
    url = "http://localhost:8000/upload"
    
    # Create a valid PNG file
    img = Image.new('RGB', (100, 100), color = 'red')
    img.save('test_image.png')
        
    files = {'file': open('test_image.png', 'rb')}
    
    try:
        print("Uploading valid image...")
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Upload failed: {e}")
    finally:
        files['file'].close()
        os.remove('test_image.png')

if __name__ == "__main__":
    test_upload_valid()
