
import requests
import os

def test_upload():
    url = "http://localhost:8000/upload"
    
    # Create a dummy text file (should fail validation but trigger logs)
    with open("test_upload.txt", "w") as f:
        f.write("This is a test file")
        
    files = {'file': open('test_upload.txt', 'rb')}
    
    try:
        print("Uploading test file...")
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Upload failed: {e}")
    finally:
        files['file'].close()
        os.remove("test_upload.txt")

if __name__ == "__main__":
    test_upload()
