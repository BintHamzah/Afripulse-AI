AfriPulse AI – Weekly Africa Startup & VC Digest (Serverless Architecture)
AfriPulse AI is an AI-powered news summarizer that curates the top Africa-focused startup and venture capital news each week—automatically.This system is deployed as a Google Cloud Function, ensuring reliable, scheduled, and cost-effective execution without manual intervention or local machines. The results are saved directly to a public Firestore database for consumption by the web frontend.

🚀 Architecture and FlowThe project follows a decoupled, serverless model:Scheduler (Cloud Scheduler): Triggers the Cloud Function weekly (via HTTP POST).Backend Worker (Cloud Function Gen2): Executes the entire Python script (fetch, filter, summarize, rank).Data Persistence (Firestore): Stores the final digest and manages subscriber emails.Frontend (Firebase Hosting): A static HTML/JS page that reads the latest digest from Firestore for immediate display.🧰 Tech Stack (Current)ComponentPurposeToolLanguageCore LogicPython 3.11+AI/LLMSummarizationGemini API (via requests)Data FetchingNews Headlines/URLsNewsAPIScrapingCleaning Article HTMLBeautiful Soup 4AutomationWeekly TriggerGoogle Cloud SchedulerExecutionServerless BackendGoogle Cloud Functions (Gen2)DatabaseDigest & SubscribersFirebase FirestoreFrontendPublic Web ReaderFirebase Hosting (Static HTML/JS)Web FrameworkGCF Entry Point / Health CheckFlaskSetup & Local Development1. Clone the repo & Install Dependenciesgit clone [https://github.com/BintHamzah/Afripulse-AI.git](https://github.com/BintHamzah/Afripulse-AI.git)
cd Afripulse-AI

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
2. Set Up Authentication (Local Backend)The Python backend uses Application Default Credentials (ADC) to authenticate as an administrator and write to your live Firestore database.# Authenticate your terminal session
gcloud auth login

# Set up credentials for the Firebase Admin SDK
gcloud auth application-default login
3. Set Environment VariablesSince the script reads API keys from the environment, set them in your terminal session. Replace the placeholders:export NEWS_API_KEY="your_news_api_key_here"
export GEMINI_API_KEY="your_gemini_api_key_here"
4. Run the Backend Worker LocallyTo simulate the scheduled run and write data to your live Firestore:# The 'main.py' file now contains the Flask-based HTTP entry point.
# We call it directly using the Python interpreter.
python -c "import main; main.generate_digest_http(None)"
Verify the data appears in the digests collection in your Firebase console.5. Run the Frontend LocallyUse the Firebase CLI to serve the static index.html page, allowing its JavaScript to securely connect to Firestore and display the digest.# If you haven't yet, initialize Firebase Hosting in the root (public directory: .)
firebase init hosting

# Start the local server
firebase emulators:start --only hosting
Open the provided local URL (http://localhost:XXXX) to view the website.💻 Deployment Commands (Cloud Shell)These steps are executed once in the Google Cloud Shell to deploy the fully automated system:1. Deploy the Cloud Functiongcloud functions deploy generate-afripulse-digest \
  --gen2 \
  --runtime python311 \
  --region us-central1 \
  --source . \
  --entry-point generate_digest_http \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars NEWS_API_KEY="${NEWS_API_KEY}",GEMINI_API_KEY="${GEMINI_API_KEY}" \
  --memory 1024MB
2. Deploy the Frontendfirebase deploy --only hosting
AuthorFatimah Hamzah (@binthamzah)Passionate about AI, QA, and automation — building tools that make information accessible and insightful for Africa’s tech ecosystem.