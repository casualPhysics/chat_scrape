import base64
import json
import datetime

import pandas as pd
from flask import session, url_for, render_template, request, redirect

from main_app import app
from flask_wtf import FlaskForm
from wtforms import SubmitField


class IGTForm(FlaskForm):
    button1 = SubmitField('Button 1')
    button2 = SubmitField('Button 2')
    button3 = SubmitField('Button 3')
    button4 = SubmitField('Button 4')


@app.route('/igt_game', methods=['GET', 'POST'])
def igt_game():
    form = IGTForm()
    state = generate_game_state()
    if form.validate_on_submit():

        # button was clicked
        if form.button1.data:
            print('hi')

        elif form.button2.data:
            print('hi')

        elif form.button3.data:
            print('hi')

        elif form.button4.data:
            print('hi')

    return render_template('harvest/igt.html', form=form, state=state)


@app.route('/submit', methods=['POST'])
def submit_game():
    # Update the game state based on the user's input
    state = update_game_state(request.form['choice'])
    session['state'] = state
    return redirect(url_for('play_game'))


def generate_game_state():
    # Generate the initial game state
    if 'state' not in session:
        state = {'score': 2000}
    else:
        state = session['state']
    return state


def update_game_state(choice):
    # Update the game state based on the user's choice
    state = session['state']
    if choice == 'correct':
        state['score'] += 1
    return state



