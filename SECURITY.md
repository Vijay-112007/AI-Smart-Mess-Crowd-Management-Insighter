# Security Policy

## Firebase Credentials Setup

**IMPORTANT: Never commit Firebase service account keys to Git!**

### Setup Instructions:

1. Download your Firebase Admin SDK credentials from Firebase Console
   - Go to Firebase Console → Project Settings → Service Accounts
   - Click "Generate New Private Key"

2. Save the file locally (e.g., `serviceAccountKey.json`)

3. Ensure the filename is listed in `.gitignore` (already configured for this repository)

4. Use environment variables or secure secret management to reference credentials

### For Local Development:

- Store credentials outside the repository or in the root directory (covered by `.gitignore`)
- Use environment variables to reference the file path:
  ```python
  import os
  import firebase_admin
  from firebase_admin import credentials
  
  # Use environment variable for credentials path
  cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'serviceAccountKey.json')
  cred = credentials.Certificate(cred_path)
  firebase_admin.initialize_app(cred)
  ```

### For Production/CI/CD:

- **GitHub Secrets**: Store credentials as repository secrets for GitHub Actions
- **Google Secret Manager**: Use Google Cloud's Secret Manager for production environments
- **Application Default Credentials**: When running on Google Cloud Platform, use ADC when possible
- **Environment Variables**: Store credentials as base64-encoded environment variables

### If Credentials Are Exposed:

If you accidentally commit Firebase credentials to Git:

1. **Immediately revoke the exposed credentials** in Google Cloud Console:
   - Go to Google Cloud Console → IAM & Admin → Service Accounts
   - Find the compromised service account
   - Delete or disable the key

2. **Generate new credentials** and store them securely (never commit to Git)

3. **Remove from Git history** using one of these tools:
   - `git filter-repo` (recommended): https://github.com/newren/git-filter-repo
   - BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/

4. **Force push** to update remote repository (coordinate with team members)

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it by:

1. **Do not** open a public issue
2. Contact the repository maintainers directly
3. Provide details about the vulnerability and steps to reproduce

We take security seriously and will respond promptly to security reports.
