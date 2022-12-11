from flask import request, session
from firebase_admin import firestore
from main_app import app

# Set up Firebase
db = firestore.client()


@app.route('/saveemail', methods=['POST'])
def save_email():
    """
    This function saves the emails that the user wants to keep.
    :return:
    """
    email_to_tap = request.form['email']
    user_super_email = session['user_email_key']
    doc_ref = db.collection(f"users/prototype_users/{user_super_email}").document(email_to_tap)
    doc_ref.set({
        "email_address": email_to_tap,
        "type": 'email_to_tap',
    })

    return "Data saved to Firebase!"


def get_user_tracked_emails(email_user_key):
    doc_ref = db.collection(f"users/prototype_users/{email_user_key}")
    doc = doc_ref.get()
    return [email.to_dict()['email_address'] for email in doc]


