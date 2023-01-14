from flask import request, session, url_for, render_template, redirect
from firebase_admin import firestore
from main_app import app


@app.route('/email_taps')
def email_taps():
    """
    This function saves the emails that the user wants to keep.
    :return:
    """
    return render_template('home/email_taps.html', segment='index',
                           email_taps_list=get_user_tracked_emails(session['user_email_key']))


@app.route('/register_email_tap')
def save_email():
    return render_template('home/register_email_tap.html')


@app.route('/save_email_tap', methods=['GET','POST'])
def save_email_tap():
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

    return redirect(url_for('email_taps'))


def get_user_tracked_emails(email_user_key):
    doc_ref = db.collection(f"users/prototype_users/{email_user_key}")
    doc = doc_ref.get()
    return [email.to_dict()['email_address'] for email in doc]
