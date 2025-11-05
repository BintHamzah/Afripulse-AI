# AfriPulse AI – Weekly Africa Startup & VC Digest (Serverless Architecture)

AfriPulse AI is an AI-powered news summarizer that curates the top Africa-focused startup and venture capital news each week—automatically. This system is deployed as a Google Cloud Function, ensuring reliable, scheduled, and cost-effective execution without manual intervention or local machines. The results are saved directly to a public Firestore database for consumption by the web frontend.

## 🚀 Architecture and Flow

The project follows a decoupled, serverless model:

- **Scheduler (Cloud Scheduler):** Triggers the Cloud Function weekly (via HTTP POST).
- **Backend Worker (Cloud Function Gen2):** Executes the entire Python script (fetch, filter, summarize, rank).
- **Data Persistence (Firestore):** Stores the final digest and manages subscriber emails.
- **Frontend (Firebase Hosting):** A static HTML/JS page that reads the latest digest from Firestore for immediate display.

## 🧰 Tech Stack (Current)

| Component             | Purpose                      | Tool                        | Language        |
| --------------------- | ---------------------------- | --------------------------- | --------------|
| Core Logic            | -                            | Python 3.11+                | -              |
| AI/LLM                | Summarization                | Gemini API (via requests)   | -              |
| Data Fetching         | News Headlines/URLs          | NewsAPI                     | -              |
| Scraping              | Cleaning Article HTML        | Beautiful Soup 4            | -              |
| Automation            | Weekly Trigger               | Google Cloud Scheduler      | -              |
| Execution             | Serverless Backend           | Google Cloud Functions (Gen2) | -              |
| Database              | Digest & Subscribers         | Firebase Firestore          | -              |
| Frontend              | Public Web Reader            | Firebase Hosting (Static HTML/JS) | -              |
| Web Framework         | GCF Entry Point / Health Check | Flask                       | -              |

## Setup & Local Development

1. **Clone the repo & Install Dependencies**
   ```bash
   git clone https://github.com/BintHamzah/Afripulse-AI.git
   cd Afripulse-AI

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r api/requirements.txt
   ```

2. **Set Up Firebase (Frontend)**

The frontend requires a Firebase configuration to connect to your Firestore database. Open `index.html` and replace the placeholder `firebaseConfig` object with your own Firebase project's configuration.

   ```javascript
   const firebaseConfig = {
       apiKey: "YOUR_API_KEY",
       authDomain: "YOUR_AUTH_DOMAIN",
       projectId: "YOUR_PROJECT_ID",
       storageBucket: "YOUR_STORAGE_BUCKET",
       messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
       appId: "YOUR_APP_ID",
       measurementId: "YOUR_MEASUREMENT_ID"
   };
   ```

3. **Set Up Authentication (Local Backend)**

The Python backend uses Application Default Credentials (ADC) to authenticate as an administrator and write to your live Firestore database.

   ```bash
   # Authenticate your terminal session
   gcloud auth login

   # Set up credentials for the Firebase Admin SDK
   gcloud auth application-default login
   ```

4. **Set Environment Variables**

Since the script reads API keys from the environment, set them in your terminal session. Replace the placeholders:

   ```bash
   export NEWS_API_KEY="your_news_api_key_here"
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

5. **Run the Backend Worker Locally**

To simulate the scheduled run and write data to your live Firestore:

   ```bash
   # The 'main.py' file now contains the Flask-based HTTP entry point.
   # We call it directly using the Python interpreter.
   python -c "from api.main import generate_digest_http; generate_digest_http(None)"
   ```

   To run in mock mode (no API keys required):

   ```bash
   export MOCK_MODE=true
   python -c "from api.main import generate_digest_http; generate_digest_http(None)"
   ```

   Verify the data appears in the `digests` collection in your Firebase console.

6. **Run the Frontend Locally**

Use the Firebase CLI to serve the static `index.html` page, allowing its JavaScript to securely connect to Firestore and display the digest.

   ```bash
   # If you haven't yet, initialize Firebase Hosting in the root (public directory: ./)
   firebase init hosting

   # Start the local server
   firebase emulators:start --only hosting
   ```

   Open the provided local URL (http://localhost:XXXX) to view the website.

7. **Running Tests**

   ```bash
   python -m unittest discover -s tests
   ```

## 💻 Deployment Commands (Cloud Shell)

These steps are executed once in the Google Cloud Shell to deploy the fully automated system:

1. **Deploy the Cloud Function**

   ```bash
   gcloud functions deploy generate-afripulse-digest \
     --gen2 \
     --runtime python311 \
     --region us-central1 \
     --source ./api \
     --entry-point generate_digest_http \
     --trigger-http \
     --allow-unauthenticated \
     --set-env-vars NEWS_API_KEY="${NEWS_API_KEY}",GEMINI_API_KEY="${GEMINI_API_KEY}" \
     --memory 1024MB
   ```

2. **Deploy the Frontend**

   ```bash
   firebase deploy --only hosting
   ```

## Author

Fatimah Hamzah (@binthamzah)

Passionate about AI, QA, and automation — building tools that make information accessible and insightful for Africa’s tech ecosystem.