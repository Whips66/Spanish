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
TENSES = ['presente', 'pretérito', 'imperfecto', 'futuro', 'condicional', 'perfecto', 'pluscuamperfecto']
TENSE_NAMES = {
    'presente': 'Presente',
    'pretérito': 'Pretérito',
    'imperfecto': 'Imperfecto',
    'futuro': 'Futuro',
    'condicional': 'Condicional',
    'perfecto': 'Pretérito Perfecto',
    'pluscuamperfecto': 'Pluscuamperfecto'
}
TENSE_DESCRIPTIONS = {
    'presente': 'Used for current actions, habitual actions, and general truths.',
    'pretérito': 'Used for completed actions in the past with a specific time frame.',
    'imperfecto': 'Used for ongoing past actions, habitual past actions, and descriptions in the past.',
    'futuro': 'Used for actions that will happen in the future.',
    'condicional': 'Used for hypothetical situations, polite requests, and future actions from a past perspective.',
    'perfecto': 'Used for actions that happened in the recent past or have relevance to the present.',
    'pluscuamperfecto': 'Used for actions that had happened before another past action.'
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
    
    # Randomly select question type: 25% each
    rand = random.random()
    if rand < 0.25:
        question_type = 'identify-tense'
    elif rand < 0.50:
        question_type = 'identify-pronoun'
    elif rand < 0.75:
        question_type = 'identify-infinitive'
    else:
        question_type = 'conjugation'
    
    if question_type == 'identify-tense':
        # Show conjugated verb, ask for the tense
        # Generate options with tense names
        all_tense_names = list(TENSE_NAMES.values())
        correct_tense_name = TENSE_NAMES[tense]
        
        # Get wrong tense names (we have 5 tenses, so get up to 3 others)
        wrong_tenses = [t for t in all_tense_names if t != correct_tense_name]
        # Since we have 5 tenses, we'll get 3 wrong ones for a total of 4 options
        if len(wrong_tenses) > 3:
            wrong_tenses = random.sample(wrong_tenses, 3)
        
        # Combine and shuffle
        all_options = [correct_tense_name] + wrong_tenses
        random.shuffle(all_options)
        
        # Ensure all options are unique
        all_options = list(dict.fromkeys(all_options))
        
        return jsonify({
            'question_type': 'identify-tense',
            'verb': verb_infinitive,
            'english': verb_data['english'],
            'pronoun': pronoun,
            'conjugated_form': correct_answer,
            'tense': tense,
            'options': all_options,
            'correct_answer': correct_tense_name
        })
    elif question_type == 'identify-pronoun':
        # Show conjugated verb, ask for the pronoun
        # Generate options with pronouns
        correct_pronoun = pronoun
        
        # Get 3 wrong pronouns
        wrong_pronouns = [p for p in PRONOUNS if p != correct_pronoun]
        wrong_pronouns = random.sample(wrong_pronouns, min(3, len(wrong_pronouns)))
        
        # Combine and shuffle
        all_options = [correct_pronoun] + wrong_pronouns
        random.shuffle(all_options)
        
        # Ensure all options are unique
        all_options = list(dict.fromkeys(all_options))
        
        return jsonify({
            'question_type': 'identify-pronoun',
            'verb': verb_infinitive,
            'english': verb_data['english'],
            'tense': tense,
            'tense_name': TENSE_NAMES[tense],
            'conjugated_form': correct_answer,
            'pronoun': pronoun,
            'options': all_options,
            'correct_answer': correct_pronoun
        })
    elif question_type == 'identify-infinitive':
        # Show conjugated verb, ask for the infinitive
        # Generate options with verb infinitives
        correct_infinitive = verb_infinitive
        
        # Get 3 wrong infinitives
        all_verbs = list(VERBS.keys())
        wrong_infinitives = [v for v in all_verbs if v != correct_infinitive]
        wrong_infinitives = random.sample(wrong_infinitives, min(3, len(wrong_infinitives)))
        
        # Combine and shuffle
        all_options = [correct_infinitive] + wrong_infinitives
        random.shuffle(all_options)
        
        # Ensure all options are unique
        all_options = list(dict.fromkeys(all_options))
        
        return jsonify({
            'question_type': 'identify-infinitive',
            'verb': verb_infinitive,
            'english': verb_data['english'],
            'tense': tense,
            'tense_name': TENSE_NAMES[tense],
            'pronoun': pronoun,
            'conjugated_form': correct_answer,
            'options': all_options,
            'correct_answer': correct_infinitive
        })
    else:
        # Standard conjugation question
        # Generate 3 wrong answers from other conjugations
        all_conjugations = []
        for t in TENSES:
            all_conjugations.extend(verb_data[t].values())
        
        # Get unique wrong answers
        wrong_answers = [conj for conj in all_conjugations if conj != correct_answer]
        # Remove duplicates
        wrong_answers = list(set(wrong_answers))
        wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
        
        # Combine and shuffle
        all_answers = [correct_answer] + wrong_answers
        random.shuffle(all_answers)
        
        # Ensure all options are unique (should be, but double check)
        all_answers = list(dict.fromkeys(all_answers))
        
        return jsonify({
            'question_type': 'conjugation',
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
    tense = data.get('tense', '')
    
    is_correct = user_answer == correct_answer
    
    response = {
        'correct': is_correct,
        'correct_answer': data.get('correct_answer')
    }
    
    # Add tense description if tense is provided
    if tense and tense in TENSE_DESCRIPTIONS:
        response['tense_description'] = TENSE_DESCRIPTIONS[tense]
        response['tense_name'] = TENSE_NAMES[tense]
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
