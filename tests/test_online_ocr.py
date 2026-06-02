import requests
import os

def test_ocr():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    image_path = os.path.join(base_dir, "docs", "live_gui_capture.png")
    print(f"Testing OCR.space on image: {image_path}")
    
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": "helloworld", # Official public test key
        "language": "eng",
        "isOverlayRequired": False,
        "scale": True,
        "OCREngine": 2
    }
    
    try:
        with open(image_path, 'rb') as f:
            files = {"file": f}
            r = requests.post(url, data=payload, files=files, timeout=15)
            
        print("Response Code:", r.status_code)
        result = r.json()
        
        # Safely convert dict to str without charmap crashes
        ascii_result_str = str(result).encode('ascii', 'ignore').decode('ascii')
        print("Full API Result (ASCII Cleaned):", ascii_result_str[:400] + "...")
        
        if "ParsedResults" in result and len(result["ParsedResults"]) > 0:
            parsed_res = result["ParsedResults"][0]
            if "ParsedText" in parsed_res:
                print("====================================")
                print("        OCR EXTRACTED TEXT          ")
                print("====================================")
                text_clean = parsed_res["ParsedText"].encode('ascii', 'ignore').decode('ascii')
                print(text_clean)
        else:
            print("Error from API:", ascii_result_str)
            
    except Exception as e:
        print("OCR Request Failed:", e)

if __name__ == "__main__":
    test_ocr()
