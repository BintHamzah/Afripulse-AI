import os
import time
from src.main import run_digest_generation # Import the main worker

def generate_digest_http(request):
    """
    HTTP entry point for the Google Cloud Function.
    Reads environment variables and triggers the main worker.
    """
    # 1. Update OS environment with keys set during deployment
    os.environ['NEWS_API_KEY'] = os.environ.get("NEWS_API_KEY")
    os.environ['GEMINI_API_KEY'] = os.environ.get("GEMINI_API_KEY")

    if not os.environ.get('NEWS_API_KEY') or not os.environ.get('GEMINI_API_KEY'):
        error_msg = "Critical: API keys are not set in the Function's environment variables."
        print(error_msg)
        return error_msg, 500 

    print("--- AfriPulse AI Cloud Function Started ---")
    start_time = time.time()
    
    # 2. Run the core logic
    result = run_digest_generation()
    
    end_time = time.time()
    
    # 3. Log status and return HTTP response
    status_message = f"Job completed. Status: {result.get('status', 'Unknown')}. Time: {end_time - start_time:.2f}s."
    print(status_message)
    print("--- AfriPulse AI Cloud Function Finished ---")
    
    # The result contains the digest data which can optionally be used for direct email trigger here.
    return status_message, 200
