import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.core.config import settings

_firebase_app = None
_db = None


def init_firebase():
    """Initialize Firebase Admin SDK."""
    global _firebase_app, _db

    if _firebase_app:
        return

    if settings.FIREBASE_SERVICE_ACCOUNT_PATH:
        cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
        _firebase_app = firebase_admin.initialize_app(cred)
    elif settings.FIREBASE_PROJECT_ID:
        _firebase_app = firebase_admin.initialize_app(options={
            "projectId": settings.FIREBASE_PROJECT_ID,
        })
    else:
        _firebase_app = firebase_admin.initialize_app()

    _db = firestore.client()


def get_db():
    """Get Firestore client instance."""
    global _db
    if _db is None:
        init_firebase()
    return _db


def verify_token(id_token: str) -> dict:
    """Verify a Firebase ID token and return the decoded claims."""
    return auth.verify_id_token(id_token)


def get_user(uid: str):
    """Get Firebase user record by UID."""
    return auth.get_user(uid)
