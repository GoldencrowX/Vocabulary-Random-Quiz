from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.args.get('level', 'A1')
    df_all = pd.read_csv('Vocabulary.csv')
    df = df_all[df_all['Level'] == level]

    if 'score' not in session:
        session['score'] = {}
    if level not in session['score']:
        session['score'][level] = 0

    if 'answered_correct' not in session:
        session['answered_correct'] = {}
    if level not in session['answered_correct']:
        session['answered_correct'][level] = []

    result = ''
    vocab = ''
    correct_meaning = ''

    if request.method == 'POST':
        vocab = request.form['vocab']
        correct_meaning = request.form['correct_meaning']
        user_input = request.form['user_input'].strip().lower()
        answered = session['answered_correct'][level]

        correct_list = [m.strip().lower() for m in correct_meaning.split(',')]

        if user_input in correct_list:
            result = 'Correct!'
            if vocab not in answered:
                answered.append(vocab)
                session['answered_correct'][level] = answered
                session['score'][level] += 1
        else:
            result = f"Incorrect!\nThe correct word for {vocab} is: {correct_meaning}"

        session.modified = True

    answered = session['answered_correct'][level]
    remaining = df[~df['Vocab'].isin(answered)]

    if request.method == 'POST' and result.startswith("Incorrect"):
        if len(remaining) > 1 and vocab in remaining['Vocab'].values:
            remaining = remaining[remaining['Vocab'] != vocab]

    if not remaining.empty:
        random_row = remaining.sample().iloc[0]
        vocab = random_row['Vocab']
        correct_meaning = str(random_row['Meaning']).strip().lower()
    else:
        result = 'Congratulations!\nYou have answered all words correctly.'
        vocab = ''
        correct_meaning = ''

    return render_template('index.html',
                           vocab=vocab,
                           correct_meaning=correct_meaning,
                           result=result,
                           level=level,
                           score=session['score'][level])

@app.route('/reset/<level>')
def reset(level):
    if 'answered_correct' in session:
        session['answered_correct'][level] = []
    if 'score' in session:
        session['score'][level] = 0
    session.modified = True
    return redirect(url_for('index', level=level))

# if __name__ == '__main__':
#     app.run(debug=True)