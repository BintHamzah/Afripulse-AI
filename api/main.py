from firebase_functions import options
options.set_global_options()
import os
import time 
import json
from flask import Flask, jsonify
from app import run_digest_generation 

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    """
    Health check endpoint for Google Cloud Run.
    """
    return "OK", 200


@app.route('/', methods=['POST'])
def generate_digest_http():
    """
    HTTP entry point for the Google Cloud Function.
    Reads environment variables and triggers the main worker (POST is used by Cloud Scheduler).
    """
    is_mock_mode = os.environ.get('MOCK_MODE') == 'true'

    if not is_mock_mode:
        # Update OS environment with keys set during deployment
        os.environ['NEWS_API_KEY'] = os.environ.get("NEWS_API_KEY")
        os.environ['GEMINI_API_KEY'] = os.environ.get("GEMINI_API_KEY")

        if not os.environ.get('NEWS_API_KEY') or not os.environ.get('GEMINI_API_KEY'):
            error_msg = "Critical: API keys are not set in the Function's environment variables."
            print(error_msg)
            return jsonify({"status": "error", "message": error_msg}), 500

    print("--- AfriPulse AI Cloud Function Triggered ---")
    start_time = time.time()
    
    try:
        if is_mock_mode:
            print("--- Running in MOCK_MODE ---")
            result = {"status": "success", "message": "Mock digest generated successfully."}
        else:
            result = run_digest_generation()
        status_code = 200
    except Exception as e:
        result = {"status": "error", "message": f"Worker execution failed: {e}"}
        status_code = 500
        print(f"FATAL ERROR: {e}")

    end_time = time.time()
    
    status_message = f"Job completed. Status: {result.get('status', 'Unknown')}. Time: {end_time - start_time:.2f}s. {result.get('message', '')}"
    print(status_message)
    print("--- AfriPulse AI Cloud Function Finished ---")
    
    return jsonify(result), status_code

# --- Health Check and Local Development Server ---
# This part is CRUCIAL for passing the Cloud Run health check.
if __name__ == '__main__':
    # When running locally, use a standard port (e.g., 8080)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
