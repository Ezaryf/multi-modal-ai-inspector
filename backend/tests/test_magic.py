
import magic
import os

def test_magic():
    try:
        print("Initializing magic...")
        mime = magic.Magic(mime=True)
        print("Magic initialized successfully.")
        
        # Create a dummy file to test
        with open("test.txt", "w") as f:
            f.write("Hello world")
            
        mime_type = mime.from_file("test.txt")
        print(f"Detected MIME type for text file: {mime_type}")
        
        os.remove("test.txt")
        
        if mime_type == "text/plain":
            print("✅ python-magic is working correctly!")
        else:
            print(f"⚠️ Unexpected MIME type: {mime_type}")
            
    except Exception as e:
        print(f"❌ Magic failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_magic()
