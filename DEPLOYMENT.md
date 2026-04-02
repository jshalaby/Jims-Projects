# Cloud Deployment Guide - Webinar Registration App

This guide will help you deploy your webinar registration app to **Streamlit Cloud** with **Google Sheets** as the database.

## Prerequisites

- GitHub account (free)
- Google account (free)
- Streamlit Cloud account (free)

## Step 1: Set Up Google Sheets API

### 1.1 Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Create a New Project**
3. Name it `Webinar Registration`
4. Click **Create**

### 1.2 Enable Google Sheets API

1. In the left menu, go to **APIs & Services** > **Library**
2. Search for **Google Sheets API**
3. Click on it and press **Enable**
4. Repeat for **Google Drive API** (search for it and enable)

### 1.3 Create Service Account

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **Service Account**
3. Fill in the form:
   - Service account name: `webinar-app`
   - Click **Create and Continue**
4. Grant the service account the role: **Editor** (for Sheets and Drive access)
5. Click **Create Key** > **JSON**
6. Download the JSON file and name it `service_account.json`

### 1.4 Create Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Name it **Webinar Registrations**
4. Share it with the service account email (from the JSON file) - give **Editor** access

## Step 2: Test Locally

1. Place `service_account.json` in your project folder
2. Run the app:
   ```bash
   streamlit run webinar_registration_cloud.py
   ```
3. Test a registration - it should save to Google Sheets

## Step 3: Push to GitHub

### 3.1 Initialize Git Repository

```bash
cd c:\Users\jshal\Projects\Jims-Projects
git init
git add .
git commit -m "Initial commit: Webinar registration app"
```

### 3.2 Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click **New Repository**
3. Name: `webinar-registration`
4. Make it **Public** (required for Streamlit Cloud free tier)
5. Click **Create Repository**

### 3.3 Push Code to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/webinar-registration.git
git branch -M main
git push -u origin main
```

**Important:** Do NOT commit `service_account.json` - it's in `.gitignore`

## Step 4: Deploy to Streamlit Cloud

### 4.1 Create Streamlit Cloud Account

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click **Sign Up**
3. Use your GitHub account to sign up

### 4.2 Deploy the App

1. Click **New App**
2. Select:
   - **Repository:** `webinar-registration`
   - **Branch:** `main`
   - **Main file path:** `webinar_registration_cloud.py`
3. Click **Deploy**

### 4.3 Add Google Secrets

1. Once deployed, click the **hamburger menu** (☰) > **Settings**
2. Go to **Secrets** tab
3. Paste your service account JSON (from `service_account.json`):

```
[google_service_account]
type = "service_account"
project_id = "YOUR_PROJECT_ID"
private_key_id = "YOUR_KEY_ID"
private_key = "YOUR_PRIVATE_KEY"
client_email = "YOUR_SERVICE_ACCOUNT_EMAIL"
client_id = "YOUR_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "YOUR_CERT_URL"
```

Or paste the entire JSON content under `[google_service_account]`

4. Click **Save** - your app will reboot

## Step 5: Test Your Cloud App

1. Your app will be live at: `https://streamlit.io/YOUR_USERNAME-webinar-registration`
2. Share the URL with users
3. Test registrations - they should appear in your Google Sheet

## Troubleshooting

**"No Google credentials found"**
- Make sure you added the secrets in Streamlit Cloud settings
- Restart the app after adding secrets

**"SpreadsheetNotFound"**
- Make sure your Google Sheet is named exactly **"Webinar Registrations"**
- Make sure the service account has access (shared with the service account email)

**"Email already exists"**
- Google Sheets doesn't enforce unique constraints by default
- Consider adding duplicate check logic if needed

## View Your Data

1. Go to [Google Sheets](https://sheets.google.com)
2. Open **Webinar Registrations**
3. All registrations will appear automatically
4. Export as CSV/Excel anytime

## Next Steps

- Add email notifications (using Gmail API)
- Add payment processing (Stripe)
- Create an admin dashboard
- Add webinar management interface
- Set up automated emails using SendGrid

## Support

For issues:
- Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud
- Google Sheets API: https://developers.google.com/sheets/api
- gspread documentation: https://docs.gspread.org
