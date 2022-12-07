from flask import request
from firebase_admin import firestore, initialize_app, credentials
from main_app import app

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('/Users/afiqhatta/chat_scrape/firebase_configs/firebase_admin_config.json')
firebase = initialize_app(cred)

# Set up Firebase
db = firestore.client()


@app.route('/save-email', methods=['POST'])
def save_email():
    email_to_tap = request.form['email']

    # Save the data to Firebase
    doc_ref = db.collection(f"users/test/{email_to_tap}").document()
    doc_ref.set({
        "data": 'hi'
    })

    return "Data saved to Firebase!"
