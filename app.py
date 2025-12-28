from flask import Flask, render_template, jsonify, request
import random
import json
import os

app = Flask(__name__)

# Load verbs from JSON file
def load_verbs():
    verbs_path = os.path.join(os.path.dirname(__file__), 'verbs.json')
    with open(verbs_path, 'r', encoding='utf-8') as f:
        return json.load(f)

VERBS = load_verbs()

PRONOUNS = ['yo', 'tú', 'él/ella', 'nosotros', 'vosotros', 'ellos']
TENSES = ['presente', 'pretérito', 'imperfecto', 'futuro', 'condicional']
TENSE_NAMES = {
    'presente': 'Present',
    'pretérito': 'Preterite',
    'imperfecto': 'Imperfect',
    'futuro': 'Future',
    'condicional': 'Conditional'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/question', methods=['GET'])
def get_question():
    """Generate a random verb conjugation question"""
    verb_infinitive = random.choice(list(VERBS.keys()))
    verb_data = VERBS[verb_infinitive]
    tense = random.choice(TENSES)
    pronoun = random.choice(PRONOUNS)
    
    correct_answer = verb_data[tense][pronoun]
    
    # Generate 3 wrong answers from other conjugations
    all_conjugations = []
    for t in TENSES:
        all_conjugations.extend(verb_data[t].values())
    
    wrong_answers = [conj for conj in all_conjugations if conj != correct_answer]
    wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
    
    # Combine and shuffle
    all_answers = [correct_answer] + wrong_answers
    random.shuffle(all_answers)
    
    return jsonify({
        'verb': verb_infinitive,
        'english': verb_data['english'],
        'pronoun': pronoun,
        'tense': tense,
        'tense_english': TENSE_NAMES[tense],
        'options': all_answers,
        'correct_answer': correct_answer
    })

@app.route('/api/check', methods=['POST'])
def check_answer():
    """Check if the submitted answer is correct"""
    data = request.json
    user_answer = data.get('answer', '').strip().lower()
    correct_answer = data.get('correct_answer', '').strip().lower()
    
    is_correct = user_answer == correct_answer
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': data.get('correct_answer')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
