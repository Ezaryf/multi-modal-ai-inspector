
import requests
import os
import time

def test_text_upload():
    url = "http://localhost:8000/upload"
    
    # Create a dummy text file
    content = "This is a test text file for the AI Inspector."
    with open("test_doc.txt", "w") as f:
        f.write(content)
        
    files = {'file': open('test_doc.txt', 'rb')}
    
    try:
        print("Uploading text file...")
        response = requests.post(url, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            media_id = data['media_id']
            print(f"Upload successful. Media ID: {media_id}")
            
            # Wait for processing
            print("Waiting for processing...")
            time.sleep(2)
            
            # Check analysis
            analysis_url = f"http://localhost:8000/media/{media_id}/analysis"
            resp = requests.get(analysis_url)
            print(f"Analysis: {resp.text}")
            
            if content in resp.text:
                print("✅ Text content found in analysis!")
            else:
                print("❌ Text content NOT found in analysis.")
                
        else:
            print("❌ Upload failed.")
            
    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        files['file'].close()
        os.remove("test_doc.txt")

if __name__ == "__main__":
    test_text_upload()
