#!/usr/bin/env python3
"""
Test the corrected JSON for /api/v1/generate-amp endpoint
"""
import requests
import json

# Server configuration
BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = f"{BASE_URL}/api/v1/generate-amp"

# Corrected JSON payload
corrected_payload = {
    "amp_template_html": "string",
    "amp_template_url": "https://cdn.suvichaar.org/processed_template_1761144693.html",
    "output_json": {
        "slide2": {
            "s2paragraph1": "Good morning and welcome to *The View From India* — your October 18, 2025 edition of the e-Paper.  \nHere are the headlines this Saturday, bringing you the latest stories shaping the nation and the world:  \n\nWould you like me to continue with a sample list of headlines in the same style?",
            "audio_url2": "https://cdn.suvichaar.org/media/tts_df81adf167804aa3b59ef2b342a01ce3.mp3",
            "voice": "alloy"
        },
        "slide3": {
            "s3paragraph1": "Seema Singh's surprise nomination rejection for Marhaura Assembly seat sparks fresh political debate, leaving parties recalculating strategies ahead of polls.",
            "audio_url3": "https://cdn.suvichaar.org/media/tts_fda63ecde51641a283b4c85077149fda.mp3",
            "voice": "alloy"
        },
        "slide4": {
            "s4paragraph1": "Seema Singh, famed in Bhojpuri cinema, now faces scrutiny as mismatches in her nomination papers spark questions over her candidacy.",
            "audio_url4": "https://cdn.suvichaar.org/media/tts_0a990859af3f4a1f95ea23be8a498b51.mp3",
            "voice": "alloy"
        },
        "slide5": {
            "s5paragraph1": "Several contenders were disqualified, reshaping the lineup and boosting chances for emerging voices in the upcoming election.",
            "audio_url5": "https://cdn.suvichaar.org/media/tts_434531d4068a4df285c97fbbda22924c.mp3",
            "voice": "alloy"
        },
        "slide6": {
            "s6paragraph1": "With the rejection confirmed, the spotlight now turns to a direct face-off between RJD's Jitendra Rai and JSP's Abhay Singh.",
            "audio_url6": "https://cdn.suvichaar.org/media/tts_59897e95ed3f410eaac4ab534c08e790.mp3",
            "voice": "alloy"
        }
    }
}

def test_corrected_json():
    """Test the corrected JSON payload"""
    print("Testing Corrected JSON for /api/v1/generate-amp")
    print("=" * 60)
    
    try:
        print("Sending request...")
        response = requests.post(ENDPOINT, json=corrected_payload, timeout=30)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS!")
            print(f"Final HTML length: {len(result.get('final_html', ''))}")
            print(f"Filename: {result.get('filename', 'N/A')}")
            
            # Show a snippet of the processed HTML
            html_snippet = result.get('final_html', '')[:300] + "..." if len(result.get('final_html', '')) > 300 else result.get('final_html', '')
            print(f"\nProcessed AMP HTML snippet:\n{html_snippet}")
            
        else:
            print(f"ERROR: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}")
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")

def show_corrected_json():
    """Show the corrected JSON structure"""
    print("\nCorrected JSON Structure:")
    print("=" * 60)
    print(json.dumps(corrected_payload, indent=2))

if __name__ == "__main__":
    show_corrected_json()
    test_corrected_json()
