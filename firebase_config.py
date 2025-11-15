"""
Firebase Configuration for Django Backend
Use this for Firebase Admin SDK or server-side Firebase features
"""

# Firebase Project Configuration
FIREBASE_PROJECT_ID = "shiku-beuty-hub"
FIREBASE_STORAGE_BUCKET = "shiku-beuty-hub.firebasestorage.app"
FIREBASE_AUTH_DOMAIN = "shiku-beuty-hub.firebaseapp.com"

# Firebase Admin SDK Configuration (if using)
# You need to download service account key from Firebase Console:
# https://console.firebase.google.com/project/shiku-beuty-hub/settings/serviceaccounts/adminsdk

# FIREBASE_SERVICE_ACCOUNT_KEY = os.path.join(BASE_DIR, 'path', 'to', 'serviceAccountKey.json')

# Example: Initialize Firebase Admin (uncomment if needed)
"""
import firebase_admin
from firebase_admin import credentials, storage, auth

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_KEY)
    firebase_admin.initialize_app(cred, {
        'storageBucket': FIREBASE_STORAGE_BUCKET,
        'projectId': FIREBASE_PROJECT_ID
    })
"""

