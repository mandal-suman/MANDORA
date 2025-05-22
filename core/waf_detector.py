from wafw00f.main import WAFW00F
import os

def detect_waf(target_url, output_folder):
    print("🔍 Running WAF detection...")
    try:
        waf = WAFW00F(target_url)
        results = waf.identwaf()

        if results:
            print(f"🔒 WAF Detected: {results}")
        else:
            print("✅ No WAF detected (or not identifiable)")

        # Save to file
        os.makedirs(output_folder, exist_ok=True)
        with open(os.path.join(output_folder, 'waf_detected.txt'), 'w') as f:
            if results:
                f.write(f"WAF Detected: {results}\n")
            else:
                f.write("No WAF Detected\n")

    except Exception as e:
        print(f"❌ Error in WAF detection: {e}")
