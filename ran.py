from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import random
# from livereload import Server

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.args.get('level', 'A1')
    df_all = pd.read_csv('Vocabulary.csv')
    df = df_all[df_all['Level'] == level]

    # ตั้งค่า session
    session.setdefault('score', {})
    session['score'].setdefault(level, 0)

    session.setdefault('answered_correct', {})
    session['answered_correct'].setdefault(level, [])

    session.setdefault('pending_retry', {})
    session['pending_retry'].setdefault(level, [])

    session.setdefault('last_vocab', {})
    session['last_vocab'].setdefault(level, '')

    result = ''
    explanation = ''
    previous_vocab = ''
    previous_meaning = ''

    if request.method == 'POST':
        vocab = request.form['vocab']
        correct_meaning = request.form['correct_meaning']
        user_input = request.form['user_input'].strip().lower()

        correct_list = [m.strip().lower() for m in correct_meaning.split(',')]
        answered = session['answered_correct'][level]
        pending_retry = session['pending_retry'][level]

        if user_input in correct_list:
            result = 'Correct!'
            if vocab not in answered:
                answered.append(vocab)
                session['score'][level] += 1
            if vocab in pending_retry:
                pending_retry.remove(vocab)
        else:
            result = 'Incorrect!'
            explanation = f"The correct word for {vocab} is: {correct_meaning}"
            if vocab not in pending_retry:
                pending_retry.append(vocab)

        session.modified = True

        # จดจำคำที่ตอบรอบก่อนเพื่อแสดงในหน้าถัดไป
        previous_vocab = vocab
        previous_meaning = correct_meaning

    # เตรียมคำใหม่
    answered = session['answered_correct'][level]
    pending_retry = session['pending_retry'][level]
    last_vocab = session['last_vocab'][level]

    # เลือกคำที่ยังไม่ได้ตอบถูก และยังไม่อยู่ใน pending_retry
    remaining = df[~df['Vocab'].isin(answered + pending_retry)]

    all_candidates = df[~df['Vocab'].isin(answered + pending_retry)]
    all_candidates = all_candidates[all_candidates['Vocab'] != last_vocab]



    if not remaining.empty:
        row = remaining.sample().iloc[0]
    elif not all_candidates.empty:
        row = all_candidates.sample().iloc[0]
    elif pending_retry:
        vocab = random.choice(pending_retry)
        row = df[df['Vocab'] == vocab].iloc[0]
    else:
    # จบเกม
        return render_template('index.html',
                           vocab='',
                           correct_meaning='',
                           part_of_speech='',
                           result='Congratulations!\nYou have answered all words correctly.',
                           explanation='',
                           level=level,
                           score=session['score'][level],
                           prev_vocab='',
                           prev_meaning='')

    new_vocab = row['Vocab']
    correct_meaning = str(row['Meaning']).strip().lower()
    part_of_speech = str(row.get('Part of Speech', 'N/A')).strip()

    # บันทึกคำที่เพิ่งแสดงล่าสุดเพื่อป้องกันซ้ำ
    session['last_vocab'][level] = new_vocab
    session.modified = True

    return render_template('index.html',
                           vocab=new_vocab,
                           correct_meaning=correct_meaning,
                           part_of_speech=part_of_speech,
                           result=result,
                           explanation=explanation,
                           level=level,
                           score=session['score'][level],
                           prev_vocab=previous_vocab,
                           prev_meaning=previous_meaning)

@app.route('/reset/<level>')
def reset(level):
    if 'answered_correct' in session:
        session['answered_correct'][level] = []
    if 'score' in session:
        session['score'][level] = 0
    if 'pending_retry' in session:
        session['pending_retry'][level] = []
    if 'last_vocab' in session:
        session['last_vocab'][level] = ''
    session.modified = True
    return redirect(url_for('index', level=level))

# if __name__ == '__main__':
#     server = Server(app.wsgi_app)
#     server.serve(debug=True)
