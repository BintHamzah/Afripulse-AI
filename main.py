import os
import time 
import json
from flask import Flask, request, jsonify
from src.app import run_digest_generation 

app = Flask(__name__)

@app.route('/', methods=['POST'])
def generate_digest_http():
    """
    HTTP entry point for the Google Cloud Function.
    Reads environment variables and triggers the main worker (POST is used by Cloud Scheduler).
    """
    # Update OS environment with keys set during deployment
    # We load them from os.environ here, so the imported modules can read them.
    os.environ['NEWS_API_KEY'] = os.environ.get("NEWS_API_KEY")
    os.environ['GEMINI_API_KEY'] = os.environ.get("GEMINI_API_KEY")

    if not os.environ.get('NEWS_API_KEY') or not os.environ.get('GEMINI_API_KEY'):
        error_msg = "Critical: API keys are not set in the Function's environment variables."
        print(error_msg)
        return jsonify({"status": "error", "message": error_msg}), 500

    print("--- AfriPulse AI Cloud Function Triggered ---")
    start_time = time.time()
    
    # 2. Run the core logic from src/orchestrator.py
    # The response object includes status, message, and URL
    try:
        result = run_digest_generation()
        status_code = 200
    except Exception as e:
        # Catch any failure during scraping/summarization
        result = {"status": "error", "message": f"Worker execution failed: {e}"}
        status_code = 500
        print(f"FATAL ERROR: {e}")

    end_time = time.time()
    
    # 3. Log status and return HTTP response
    status_message = f"Job completed. Status: {result.get('status', 'Unknown')}. Time: {end_time - start_time:.2f}s. {result.get('message', '')}"
    print(status_message)
    print("--- AfriPulse AI Cloud Function Finished ---")
    
    return jsonify(result), status_code

# --- Health Check and Local Development Server ---
# This part is CRUCIAL for passing the Cloud Run health check.
if __name__ == '__main__':
    # When running locally, use a standard port (e.g., 8080)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Expose the Flask application object for the Cloud Function environment
# NOTE: This is how Gunicorn/Cloud Run knows which app to run
if __name__ != '__main__':
    pass
