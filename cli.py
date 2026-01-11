import argparse
import json
import requests
import sys
API_URL = "http://localhost:8000/analyze"
def main():
    parser = argparse.ArgumentParser(description="Guardrails Gateway CLI")
    parser.add_argument("--input", required=True, help="Path to input JSON file")
    parser.add_argument("--output", required=True, help="Path to save output JSON")
    args = parser.parse_args()
    try:
        with open(args.input, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{args.input}' is not valid JSON.")
        sys.exit(1)
    try:
        print(f"Sending request to {API_URL}...")
        response = requests.post(API_URL, json=data)
        response.raise_for_status() # Raise error for 4xx/5xx
        result = response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Is it running? (uvicorn app.main:app --reload)")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        sys.exit(1)
    # 4. Write Output File
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Success! Analysis saved to {args.output}")
    print(f"Decision: {result.get('decision')}")
    print(f"Risk Score: {result.get('risk_score')}")
if __name__ == "__main__":
    main()