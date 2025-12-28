# PractiVerbo 🎯

A fun and interactive web application for practicing Spanish verb conjugation, inspired by Duolingo's engaging learning approach.

## Features

- 🎮 **Gamified Learning**: Score points, build streaks, and track your best performance
- 📊 **Progress Tracking**: Visual progress bar and real-time statistics
- 🤖 **Animated Mascot**: Friendly robot character that celebrates correct answers and encourages you when wrong
- 🎯 **Four Question Types** (25% each):
  - Conjugation questions: Conjugate verbs for given tense and pronoun
  - Identify tense questions: Identify which tense a conjugated verb is using
  - Identify pronoun questions: Determine which pronoun matches the conjugation
  - Identify infinitive questions: Match a conjugation to its base verb
- ⚡ **Instant Feedback**: Immediate confirmation with encouraging messages and tense usage explanations
- 💡 **Smart Hints**: Context-aware hints for wrong answers (regular verb patterns, irregular verb tips, pronoun clues)
- 🌟 **50 Common Verbs**: Practice the most frequently used Spanish verbs
- 📚 **10 Tenses**: Comprehensive coverage including simple, compound, and subjunctive tenses
- 📱 **Responsive Design**: Works great on desktop and mobile devices
- 🎓 **Educational**: Learn what each tense is used for with detailed descriptions
- 🌐 **Spanish Interface**: Tense names displayed in Spanish for authentic learning

## Verb Coverage

The application includes **50 of the most commonly used Spanish verbs**:

- ser (to be)
- estar (to be - location/condition)
- haber (to have - auxiliary)
- tener (to have)
- hacer (to do/make)
- poder (to be able to)
- decir (to say/tell)
- ir (to go)
- ver (to see)
- dar (to give)
- saber (to know)
- querer (to want)
- llegar (to arrive)
- pasar (to pass/happen)
- deber (to owe/must)
- poner (to put)
- parecer (to seem)
- quedar (to stay/remain)
- creer (to believe)
- hablar (to speak)
- llevar (to carry/wear)
- dejar (to leave/let)
- seguir (to follow/continue)
- encontrar (to find)
- llamar (to call)
- venir (to come)
- pensar (to think)
- salir (to leave/go out)
- volver (to return)
- tomar (to take)
- conocer (to know/meet)
- vivir (to live)
- sentir (to feel)
- tratar (to treat/try)
- mirar (to look)
- contar (to count/tell)
- empezar (to begin)
- esperar (to wait/hope)
- buscar (to search)
- existir (to exist)
- entrar (to enter)
- trabajar (to work)
- escribir (to write)
- perder (to lose)
- producir (to produce)
- abrir (to open)
- cerrar (to close)
- recibir (to receive)
- volver (to return)
- entender (to understand)

## Tenses Covered

The app covers **10 verb tenses** including **indicative** and **subjunctive moods**:

### Indicative Mood (8 tenses)

1. **Presente** (Present) - Current actions, habitual actions, and general truths
2. **Pretérito** (Preterite) - Completed actions in the past with a specific time frame
3. **Imperfecto** (Imperfect) - Ongoing past actions, habitual past actions, and descriptions
4. **Futuro** (Future) - Actions that will happen in the future
5. **Condicional** (Conditional) - Hypothetical situations, polite requests, and future actions from a past perspective
6. **Pretérito Perfecto** (Present Perfect) - Actions that happened in the recent past or have relevance to the present
7. **Pluscuamperfecto** (Past Perfect/Pluperfect) - Actions that had happened before another past action
8. **Futuro Perfecto** (Future Perfect) - Actions that will have been completed by a certain point in the future

### Subjunctive Mood (2 tenses)

9. **Presente de Subjuntivo** (Present Subjunctive) - Express wishes, doubts, emotions, recommendations, and uncertainty in present or future contexts. Common after expressions like "espero que...", "es importante que...", "dudo que..."
10. **Imperfecto de Subjuntivo** (Imperfect Subjunctive) - Used for hypothetical situations, wishes in the past, "if" clauses (si clauses), and polite requests. Essential for expressing contrary-to-fact statements

## Installation

1. Make sure you have Python 3.7+ installed

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Start practicing! 🎉

## Running Tests

The application includes comprehensive unit and integration tests.

### Run all tests:
```bash
python run_tests.py
```

### Run specific test files:
```bash
# Unit tests
python -m unittest test_app.py

# Integration tests
python -m unittest test_integration.py
```

### Test Coverage

The test suite includes:
- **39 tests** covering all functionality
- **Unit tests** for verb database, Flask routes, and API endpoints
- **Integration tests** for complete user workflows
- **Coverage tests** for all 50 verbs, 10 tenses, and 6 pronouns
- **Question type tests** for all 4 question types (conjugation, identify-tense, identify-pronoun, identify-infinitive)

Test categories:
- Verb database structure and validation
- JSON file integrity
- Flask API endpoints (`/`, `/api/question`, `/api/check`)
- Question generation and randomization
- Answer checking (correct/incorrect/case-insensitive)
- Dual question type functionality
- Tense identification questions
- Complete user workflows
- Edge cases and error handling

## How to Play

### Conjugation Questions (25% of questions)
1. **Read the Verb**: See the infinitive form and its English translation
2. **Check the Tense**: See which tense is displayed (in Spanish)
3. **See the Pronoun**: Look at which pronoun you need to conjugate for
4. **Select Your Answer**: Click the correct conjugation from the options
5. **Get Feedback**: Receive immediate feedback with tense usage description and hints if wrong

### Identify Tense Questions (25% of questions)
1. **Read the Verb**: See the infinitive form and its English translation
2. **See the Conjugation**: A fully conjugated verb form is shown with its pronoun
3. **Identify the Tense**: Choose which Spanish tense the conjugation belongs to
4. **Get Feedback**: Learn about the tense usage and get hints about tense characteristics

### Identify Pronoun Questions (25% of questions)
1. **Read the Verb**: See the infinitive form and its English translation
2. **Check the Tense**: See which tense is displayed (in Spanish)
3. **See the Conjugation**: A fully conjugated verb form is shown
4. **Identify the Pronoun**: Choose which pronoun matches the conjugation
5. **Get Feedback**: Learn with hints about pronoun-verb endings

### Identify Infinitive Questions (25% of questions)
1. **See the Conjugation**: A fully conjugated verb form is shown with tense and pronoun
2. **Identify the Verb**: Choose which infinitive (base form) the conjugation comes from
3. **Get Feedback**: Learn about verb patterns and irregularities

After each question, you'll see:
- ✅ or ❌ Immediate feedback with animated mascot reaction
- 💡 Helpful hints if you answered incorrectly
- 📖 A description of what the tense is used for (in English)
- 📊 Updated score and streak counters

## Tips

- Focus on one tense at a time when starting out
- Pay attention to irregular verbs - they have unique patterns
- **Subjunctive tips**: Remember the "opposite vowel" rule (ar→e, er/ir→a) for presente subjuntivo
- **Subjunctive triggers**: Look for phrases like "espero que", "es importante que", "si yo fuera"
- Read the hints provided after wrong answers to learn patterns
- Read the tense descriptions after each answer to understand usage
- Use the streak counter as motivation to maintain accuracy
- The variety of question types helps reinforce learning from different angles
- Practice regularly for best results
- Watch the mascot celebrate your progress!
 3.12)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Modern CSS with gradients, animations (including animated mascot), and responsive design
- **Data Storage**: JSON file (50 verbs × 10 tenses × 6 pronouns = 3000 conjugations) with UTF-8 encoding
- **Local Storage**: Browser LocalStorage for best streak persistence
- **Testing**: Python unittest framework with 39 comprehensive tests
- **Version Control**: Git

The project includes VS Code configuration files:
- **.vscode/tasks.json**: Task for running the Flask app
- **.vscode/launch.json**: Debug configurations for Flask and Python files

You can run or debug the application directly from VS Code using F5 or the Run menu.

## Future Enhancements

Potential features to add:
- Additional subjunctive tenses (perfecto de subjuntivo, pluscuamperfecto de subjuntivo)
- Imperative mood (commands)
- Difficulty levels (beginner/intermediate/advanced)
- Timed challenges and speed rounds
- Verb conjugation reference charts
- Custom verb lists and focus areas
- User accounts and progress saving
- Audio pronunciation
- Spaced repetition algorithm
- Mobile app version

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Storage**: LocalStorage for best streak persistence

---

¡Buena suerte! (Good luck!) 🌟
