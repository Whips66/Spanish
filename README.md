# Spanish Verb Conjugation Practice 🎯

A fun and interactive web application for practicing Spanish verb conjugation, inspired by Duolingo's engaging learning approach.

## Features

- 🎮 **Gamified Learning**: Score points, build streaks, and track your best performance
- 📊 **Progress Tracking**: Visual progress bar and real-time statistics
- 🎯 **Dual Question Types**: 
  - Conjugation questions (75%): Conjugate verbs for given tense and pronoun
  - Identify tense questions (25%): Identify which tense a conjugated verb is using
- ⚡ **Instant Feedback**: Immediate confirmation with encouraging messages and tense usage explanations
- 🌟 **25 Common Verbs**: Practice the most frequently used Spanish verbs
- 📚 **7 Tenses**: Comprehensive coverage from present to compound past tenses
- 📱 **Responsive Design**: Works great on desktop and mobile devices
- 🎓 **Educational**: Learn what each tense is used for with detailed descriptions
- 🌐 **Spanish Interface**: Tense names displayed in Spanish for authentic learning

## Verb Coverage

The application includes **25 of the most commonly used Spanish verbs**:

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

## Tenses Covered

The app covers **7 verb tenses**:

1. **Presente** (Present) - Current actions, habitual actions, and general truths
2. **Pretérito** (Preterite) - Completed actions in the past with a specific time frame
3. **Imperfecto** (Imperfect) - Ongoing past actions, habitual past actions, and descriptions
4. **Futuro** (Future) - Actions that will happen in the future
5. **Condicional** (Conditional) - Hypothetical situations, polite requests, and future actions from a past perspective
6. **Pretérito Perfecto** (Present Perfect) - Actions that happened in the recent past or have relevance to the present
7. **Pluscuamperfecto** (Past Perfect/Pluperfect) - Actions that had happened before another past action

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
- **26 tests** covering all functionality
- **Unit tests** for verb database, Flask routes, and API endpoints
- **Integration tests** for complete user workflows
- **Coverage tests** for all verbs, tenses, and pronouns
- **Question type tests** for both conjugation and identify-tense questions

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

### Conjugation Questions (75% of questions)
1. **Read the Verb**: See the infinitive form and its English translation
2. **Check the Tense**: See which tense is displayed (in Spanish)
3. **See the Pronoun**: Look at which pronoun you need to conjugate for
4. **Select Your Answer**: Click the correct conjugation from the options
5. **Get Feedback**: Receive immediate feedback with tense usage description

### Identify Tense Questions (25% of questions)
1. **Read the Verb**: See the infinitive form and its English translation
2. **See the Conjugation**: A fully conjugated verb form is shown with its pronoun
3. **Identify the Tense**: Choose which Spanish tense the conjugation belongs to
4. **Get Feedback**: Learn about the tense usage after answering

After each question, you'll see:
- ✅ or ❌ Immediate feedback on your answer
- 📖 A description of what the tense is used for (in English)
- 📊 Updated score and streak counters

## Tips

- Focus on one tense at a time when starting out
- Pay attention to irregular verbs - they have unique patterns
- Read the tense descriptions after each answer to understand usage
- Use the streak counter as motivation to maintain accuracy
- The identify-tense questions help you recognize verb forms in context
- Practice regularly for best results
 3.12)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Modern CSS with gradients, animations, and responsive design
- **Data Storage**: JSON file with UTF-8 encoding for Spanish characters
- **Local Storage**: Browser LocalStorage for best streak persistence
- **Testing**: Python unittest framework
- **Version Control**: Git

The project includes VS Code configuration files:
- **.vscode/tasks.json**: Task for running the Flask app
- **.vscode/launch.json**: Debug configurations for Flask and Python files

You can run or debug the application directly from VS Code using F5 or the Run menu.

## Future Enhancements

Potential features to add:
- Subjunctive mood tenses
- Difficulty levels (beginner/intermediate/advanced)
- Timed challenges and speed rounds
- Verb conjugation reference charts
- Custom verb lists and focus areas
- User accounts and progress saving
- Audio pronunciation
- Hints system
- Spaced repetition algorithm
- Mobile app version

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients and animations
- **Storage**: LocalStorage for best streak persistence

---

¡Buena suerte! (Good luck!) 🌟
