import argparse
import json
import requests
import sys

API_URL = "http://localhost:8000/analyze"

def main():
    parser = argparse.ArgumentParser(description="Guardrails Gateway CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a request")
    analyze_parser.add_argument("--input", required=True, help="Path to input JSON file")
    analyze_parser.add_argument("--output", required=True, help="Path to save output JSON")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        run_analyze(args.input, args.output)
    try:
        with open(input_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{input_path}' is not valid JSON.")
        sys.exit(1)
    try:
        print(f"Sending request to {API_URL}...")
        response = requests.post(API_URL, json=data)
        response.raise_for_status() 
        result = response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Is it running? (uvicorn app.main:app --reload)")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        sys.exit(1)

    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Success! Analysis saved to {output_path}")
    print(f"Decision: {result.get('decision')}")
    print(f"Risk Score: {result.get('risk_score')}")

if __name__ == "__main__":
    main()