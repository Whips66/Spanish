// Game state
let currentQuestion = null;
let score = 0;
let streak = 0;
let bestStreak = 0;
let questionsAnswered = 0;
let isAnswered = false;

// Session state
const SESSION_LENGTH = 20;
let sessionActive = false;
let sessionQuestions = 0;
let sessionCorrect = 0;
let sessionIncorrect = 0;
let sessionData = {
    tenseErrors: {},
    questionTypeErrors: {},
    verbErrors: {}
};

// DOM elements
const infinitiveEl = document.getElementById('infinitive');
const englishEl = document.getElementById('english');
const tenseBadgeEl = document.getElementById('tense-badge');
const pronounEl = document.getElementById('pronoun');
const optionsEl = document.getElementById('options');
const feedbackEl = document.getElementById('feedback');
const nextBtnEl = document.getElementById('next-btn');
const scoreEl = document.getElementById('score');
const streakEl = document.getElementById('streak');
const bestStreakEl = document.getElementById('best-streak');
const progressBarEl = document.getElementById('progress-bar');
const mascotEl = document.getElementById('mascot');

// Load a new question
async function loadQuestion() {
    // Check if session is complete
    if (sessionActive && sessionQuestions >= SESSION_LENGTH) {
        return; // Don't load more questions
    }
    
    try {
        const response = await fetch('/api/question');
        currentQuestion = await response.json();
        
        // Update UI based on question type
        // For identify-infinitive, hide the verb name (that's the answer!)
        if (currentQuestion.question_type === 'identify-infinitive') {
            infinitiveEl.textContent = '???';
            englishEl.textContent = '';
        } else {
            infinitiveEl.textContent = currentQuestion.verb;
            englishEl.textContent = currentQuestion.english;
        }
        
        if (currentQuestion.question_type === 'identify-tense') {
            // Identify tense question
            tenseBadgeEl.textContent = '❓ Identify the Tense';
            tenseBadgeEl.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
            
            pronounEl.textContent = currentQuestion.pronoun;
            
            // Show conjugated form in question
            document.querySelector('.question h2').textContent = 'What tense is this conjugation?';
            
            // Create a special display for the conjugated form
            const conjugatedDisplay = document.createElement('div');
            conjugatedDisplay.className = 'conjugated-display';
            conjugatedDisplay.style.fontSize = '2rem';
            conjugatedDisplay.style.fontWeight = 'bold';
            conjugatedDisplay.style.color = '#667eea';
            conjugatedDisplay.style.padding = '20px';
            conjugatedDisplay.style.background = '#f8f9ff';
            conjugatedDisplay.style.borderRadius = '10px';
            conjugatedDisplay.style.marginTop = '15px';
            conjugatedDisplay.textContent = currentQuestion.conjugated_form;
            
            // Clear pronoun element and add conjugated form there
            const questionSection = document.querySelector('.question');
            const existingConjugated = questionSection.querySelector('.conjugated-display');
            if (existingConjugated) {
                existingConjugated.remove();
            }
            questionSection.appendChild(conjugatedDisplay);
        } else if (currentQuestion.question_type === 'identify-pronoun') {
            // Identify pronoun question
            tenseBadgeEl.textContent = currentQuestion.tense_name;
            tenseBadgeEl.style.background = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
            
            // Show conjugated form in question
            document.querySelector('.question h2').textContent = 'Which pronoun is this conjugation for?';
            
            // Create a special display for the conjugated form
            const conjugatedDisplay = document.createElement('div');
            conjugatedDisplay.className = 'conjugated-display';
            conjugatedDisplay.style.fontSize = '2rem';
            conjugatedDisplay.style.fontWeight = 'bold';
            conjugatedDisplay.style.color = '#00a8cc';
            conjugatedDisplay.style.padding = '20px';
            conjugatedDisplay.style.background = '#f0faff';
            conjugatedDisplay.style.borderRadius = '10px';
            conjugatedDisplay.style.marginTop = '15px';
            conjugatedDisplay.textContent = currentQuestion.conjugated_form;
            
            // Clear pronoun element and add conjugated form there
            const questionSection = document.querySelector('.question');
            const existingConjugated = questionSection.querySelector('.conjugated-display');
            if (existingConjugated) {
                existingConjugated.remove();
            }
            questionSection.appendChild(conjugatedDisplay);
            
            // Hide pronoun display since that's what they're guessing
            pronounEl.textContent = '?';
        } else if (currentQuestion.question_type === 'identify-infinitive') {
            // Identify infinitive question
            tenseBadgeEl.textContent = currentQuestion.tense_name;
            tenseBadgeEl.style.background = 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)';
            
            // Show conjugated form in question
            document.querySelector('.question h2').textContent = 'What is the infinitive of this verb?';
            
            // Create a special display for the conjugated form
            const conjugatedDisplay = document.createElement('div');
            conjugatedDisplay.className = 'conjugated-display';
            conjugatedDisplay.style.fontSize = '2rem';
            conjugatedDisplay.style.fontWeight = 'bold';
            conjugatedDisplay.style.color = '#d83f87';
            conjugatedDisplay.style.padding = '20px';
            conjugatedDisplay.style.background = '#fff5f8';
            conjugatedDisplay.style.borderRadius = '10px';
            conjugatedDisplay.style.marginTop = '15px';
            conjugatedDisplay.textContent = currentQuestion.conjugated_form;
            
            // Clear pronoun element and add conjugated form there
            const questionSection = document.querySelector('.question');
            const existingConjugated = questionSection.querySelector('.conjugated-display');
            if (existingConjugated) {
                existingConjugated.remove();
            }
            questionSection.appendChild(conjugatedDisplay);
            
            // Show pronoun for context
            pronounEl.textContent = currentQuestion.pronoun;
        } else {
            // Standard conjugation question
            tenseBadgeEl.textContent = currentQuestion.tense_english;
            tenseBadgeEl.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
            
            document.querySelector('.question h2').textContent = 'Conjugate for:';
            pronounEl.textContent = currentQuestion.pronoun;
            
            // Remove conjugated display if it exists
            const existingConjugated = document.querySelector('.conjugated-display');
            if (existingConjugated) {
                existingConjugated.remove();
            }
        }
        
        // Create option buttons
        optionsEl.innerHTML = '';
        currentQuestion.options.forEach(option => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.textContent = option;
            btn.addEventListener('click', () => selectAnswer(option, btn));
            optionsEl.appendChild(btn);
        });
        
        // Reset state
        feedbackEl.classList.remove('show', 'correct', 'incorrect');
        feedbackEl.textContent = '';
        nextBtnEl.style.display = 'none';
        isAnswered = false;
        
        // Update progress bar
        updateProgressBar();
        
    } catch (error) {
        console.error('Error loading question:', error);
        infinitiveEl.textContent = 'Error loading question';
    }
}

// Handle answer selection
async function selectAnswer(answer, button) {
    if (isAnswered) return;
    isAnswered = true;
    
    // Disable all buttons
    const allButtons = document.querySelectorAll('.option-btn');
    allButtons.forEach(btn => btn.disabled = true);
    
    // Check answer
    const isCorrect = answer === currentQuestion.correct_answer;
    
    // Send answer to server for validation and get tense description
    try {
        const response = await fetch('/api/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answer: answer,
                correct_answer: currentQuestion.correct_answer,
                tense: currentQuestion.tense,
                verb: currentQuestion.verb,
                pronoun: currentQuestion.pronoun,
                question_type: currentQuestion.question_type,
                all_correct_answers: currentQuestion.all_correct_answers || []
            })
        });
        const result = await response.json();
        
        // Update button styling
        if (isCorrect) {
            button.classList.add('correct');
            
            // For identify-infinitive, reveal the verb name and English after answering
            if (currentQuestion.question_type === 'identify-infinitive') {
                document.querySelector('.infinitive').textContent = currentQuestion.correct_answer;
                document.querySelector('.english').textContent = currentQuestion.english;
            }
            
            showFeedback(true, result);
            updateScore(true);
            updateMascot('happy');
            playSound('correct');
        } else {
            button.classList.add('incorrect');
            
            // For identify-infinitive, reveal the verb name and English after answering
            if (currentQuestion.question_type === 'identify-infinitive') {
                document.querySelector('.infinitive').textContent = currentQuestion.correct_answer;
                document.querySelector('.english').textContent = currentQuestion.english;
            }
            
            showFeedback(false, result);
            updateScore(false);
            updateMascot('sad');
            playSound('incorrect');
            
            // Highlight correct answer(s)
            allButtons.forEach(btn => {
                // For identify-pronoun, highlight all correct answers
                if (currentQuestion.question_type === 'identify-pronoun' && 
                    currentQuestion.all_correct_answers && 
                    currentQuestion.all_correct_answers.includes(btn.textContent)) {
                    btn.classList.add('correct');
                } else if (btn.textContent === currentQuestion.correct_answer) {
                    btn.classList.add('correct');
                }
            });
        }
    } catch (error) {
        console.error('Error checking answer:', error);
        // Fallback to local check
        if (isCorrect) {
            button.classList.add('correct');
            
            // For identify-infinitive, reveal the verb name and English after answering
            if (currentQuestion.question_type === 'identify-infinitive') {
                document.querySelector('.infinitive').textContent = currentQuestion.correct_answer;
                document.querySelector('.english').textContent = currentQuestion.english;
            }
            
            showFeedback(true, {});
            updateScore(true);
            updateMascot('happy');
            playSound('correct');
        } else {
            button.classList.add('incorrect');
            
            // For identify-infinitive, reveal the verb name and English after answering
            if (currentQuestion.question_type === 'identify-infinitive') {
                document.querySelector('.infinitive').textContent = currentQuestion.correct_answer;
                document.querySelector('.english').textContent = currentQuestion.english;
            }
            
            showFeedback(false, {});
            updateScore(false);
            updateMascot('sad');
            playSound('incorrect');
            
            allButtons.forEach(btn => {
                if (btn.textContent === currentQuestion.correct_answer) {
                    btn.classList.add('correct');
                }
            });
        }
    }
    
    // Show next button
    nextBtnEl.style.display = 'block';
    questionsAnswered++;
    
    // Track session progress
    if (sessionActive) {
        sessionQuestions++;
        if (isCorrect) {
            sessionCorrect++;
        } else {
            sessionIncorrect++;
            // Track errors by tense, question type, and verb
            if (currentQuestion.tense) {
                sessionData.tenseErrors[currentQuestion.tense] = (sessionData.tenseErrors[currentQuestion.tense] || 0) + 1;
            }
            sessionData.questionTypeErrors[currentQuestion.question_type] = (sessionData.questionTypeErrors[currentQuestion.question_type] || 0) + 1;
            sessionData.verbErrors[currentQuestion.verb] = (sessionData.verbErrors[currentQuestion.verb] || 0) + 1;
        }
        
        // Check if session is complete
        if (sessionQuestions >= SESSION_LENGTH) {
            setTimeout(() => showSessionSummary(), 1500);
        }
    }
}

// Show feedback message
function showFeedback(isCorrect, result = {}) {
    const correctMessages = [
        '¡Excelente! 🎉',
        '¡Perfecto! ⭐',
        '¡Muy bien! 👏',
        '¡Increíble! 🌟',
        '¡Fantástico! 🎊',
    ];
    
    const incorrectMessages = [
        'Not quite! Try again 💪',
        'Keep practicing! 📚',
        'Almost there! 🎯',
        'You\'ll get it next time! 🚀',
    ];
    
    const messageList = isCorrect ? correctMessages : incorrectMessages;
    let message = messageList[Math.floor(Math.random() * messageList.length)];
    
    if (!isCorrect) {
        let correctAnswerText = '';
        if (currentQuestion.question_type === 'identify-tense') {
            correctAnswerText = `Correct tense: ${currentQuestion.correct_answer}`;
        } else if (currentQuestion.question_type === 'identify-pronoun') {
            // Show all correct answers if there are multiple
            if (currentQuestion.all_correct_answers && currentQuestion.all_correct_answers.length > 1) {
                correctAnswerText = `Correct pronouns: ${currentQuestion.all_correct_answers.join(' or ')}`;
            } else {
                correctAnswerText = `Correct pronoun: ${currentQuestion.correct_answer}`;
            }
        } else if (currentQuestion.question_type === 'identify-infinitive') {
            correctAnswerText = `Correct verb: ${currentQuestion.correct_answer} (${currentQuestion.english})`;
        } else {
            correctAnswerText = `Correct answer: ${currentQuestion.correct_answer}`;
        }
        
        message += `<div class="correct-answer">${correctAnswerText}</div>`;
        
        // Add hint if available
        if (result.hint) {
            message += `<div style="margin-top: 8px; font-size: 0.9rem;">${result.hint}</div>`;
        }
    }
    
    // Add tense description if available
    if (result.tense_description && result.tense_name) {
        message += `<div style="margin-top: 8px; font-size: 0.9rem; font-style: italic;">${result.tense_name}: ${result.tense_description}</div>`;
    }
    
    feedbackEl.innerHTML = message;
    feedbackEl.classList.add('show', isCorrect ? 'correct' : 'incorrect');
}

// Update score and streak
function updateScore(isCorrect) {
    if (isCorrect) {
        score += 10;
        streak++;
        if (streak > bestStreak) {
            bestStreak = streak;
            localStorage.setItem('bestStreak', bestStreak);
        }
    } else {
        streak = 0;
    }
    
    scoreEl.textContent = score;
    streakEl.textContent = streak;
    bestStreakEl.textContent = bestStreak;
    
    // Animate score
    scoreEl.style.transform = 'scale(1.3)';
    setTimeout(() => {
        scoreEl.style.transform = 'scale(1)';
    }, 200);
}

// Update progress bar
function updateProgressBar() {
    if (sessionActive) {
        updateSessionProgress();
    } else {
        const progress = (questionsAnswered % 10) * 10;
        progressBarEl.style.width = progress + '%';
    }
}

// Update mascot state
function updateMascot(state) {
    mascotEl.className = 'mascot ' + state;
    
    // Reset animation after it completes
    setTimeout(() => {
        mascotEl.className = 'mascot';
    }, 600);
}

// Play sound effect (visual feedback in absence of audio)
function playSound(type) {
    // Visual feedback
    document.body.style.animation = type === 'correct' 
        ? 'none' 
        : 'none';
    
    // Force reflow to restart animation
    setTimeout(() => {
        document.body.style.animation = '';
    }, 10);
}

// Load best streak from localStorage
function loadBestStreak() {
    const saved = localStorage.getItem('bestStreak');
    if (saved) {
        bestStreak = parseInt(saved);
        bestStreakEl.textContent = bestStreak;
    }
}

// Event listeners
nextBtnEl.addEventListener('click', loadQuestion);
document.getElementById('start-session-btn').addEventListener('click', startSession);
document.getElementById('close-summary-btn').addEventListener('click', closeSessionSummary);
document.getElementById('restart-session-btn').addEventListener('click', restartSession);

// Session management functions
function startSession() {
    sessionActive = true;
    sessionQuestions = 0;
    sessionCorrect = 0;
    sessionIncorrect = 0;
    sessionData = {
        tenseErrors: {},
        questionTypeErrors: {},
        verbErrors: {}
    };
    
    // Update UI
    document.getElementById('session-panel').style.display = 'none';
    document.getElementById('session-progress').style.display = 'block';
    updateSessionProgress();
    
    // Reset score for session
    score = 0;
    streak = 0;
    scoreEl.textContent = score;
    streakEl.textContent = streak;
    
    loadQuestion();
}

function updateSessionProgress() {
    const progressText = document.getElementById('session-progress-text');
    progressText.textContent = `Question ${sessionQuestions}/${SESSION_LENGTH}`;
    
    const progressPercent = (sessionQuestions / SESSION_LENGTH) * 100;
    progressBarEl.style.width = progressPercent + '%';
}

function showSessionSummary() {
    const modal = document.getElementById('session-summary-modal');
    const accuracy = sessionCorrect > 0 ? Math.round((sessionCorrect / SESSION_LENGTH) * 100) : 0;
    
    // Update summary stats
    document.getElementById('summary-total').textContent = SESSION_LENGTH;
    document.getElementById('summary-correct').textContent = sessionCorrect;
    document.getElementById('summary-incorrect').textContent = sessionIncorrect;
    document.getElementById('summary-accuracy').textContent = accuracy + '%';
    document.getElementById('summary-score').textContent = score;
    
    // Generate feedback
    const feedbackEl = document.getElementById('summary-feedback');
    feedbackEl.innerHTML = generateFeedback(accuracy);
    
    // Show modal
    modal.style.display = 'flex';
}

function generateFeedback(accuracy) {
    let feedback = '<div class="feedback-section">';
    
    // Overall performance
    if (accuracy >= 90) {
        feedback += '<h3>🎉 ¡Excelente!</h3><p>Outstanding work! You have a strong grasp of Spanish verb conjugation.</p>';
    } else if (accuracy >= 75) {
        feedback += '<h3>🌟 ¡Muy bien!</h3><p>Great job! You\'re doing really well with your conjugations.</p>';
    } else if (accuracy >= 60) {
        feedback += '<h3>💪 Good effort!</h3><p>You\'re making progress! Keep practicing to improve.</p>';
    } else {
        feedback += '<h3>📚 Keep going!</h3><p>Don\'t give up! Consistent practice will help you improve.</p>';
    }
    feedback += '</div>';
    
    // Weak areas
    if (sessionIncorrect > 0) {
        feedback += '<div class="feedback-section">';
        feedback += '<h3>💡 Areas to Focus On:</h3>';
        feedback += '<ul class="feedback-list">';
        
        // Most problematic tenses
        const tenseErrorsArray = Object.entries(sessionData.tenseErrors).sort((a, b) => b[1] - a[1]);
        if (tenseErrorsArray.length > 0) {
            const topTense = tenseErrorsArray[0];
            feedback += `<li><strong>Tense:</strong> Practice more with <em>${topTense[0]}</em> (${topTense[1]} error${topTense[1] > 1 ? 's' : ''})</li>`;
        }
        
        // Most problematic question types
        const qtErrorsArray = Object.entries(sessionData.questionTypeErrors).sort((a, b) => b[1] - a[1]);
        if (qtErrorsArray.length > 0) {
            const topQT = qtErrorsArray[0];
            const qtNames = {
                'conjugation': 'Conjugation',
                'identify-tense': 'Tense Identification',
                'identify-pronoun': 'Pronoun Identification',
                'identify-infinitive': 'Infinitive Identification'
            };
            feedback += `<li><strong>Question Type:</strong> Work on <em>${qtNames[topQT[0]]}</em> questions (${topQT[1]} error${topQT[1] > 1 ? 's' : ''})</li>`;
        }
        
        // Most problematic verbs
        const verbErrorsArray = Object.entries(sessionData.verbErrors).sort((a, b) => b[1] - a[1]).slice(0, 3);
        if (verbErrorsArray.length > 0) {
            feedback += '<li><strong>Verbs to review:</strong> ';
            feedback += verbErrorsArray.map(v => `<em>${v[0]}</em>`).join(', ');
            feedback += '</li>';
        }
        
        feedback += '</ul></div>';
    }
    
    // Tips
    feedback += '<div class="feedback-section">';
    feedback += '<h3>🎯 Tips for Improvement:</h3>';
    feedback += '<ul class="feedback-list">';
    
    if (accuracy < 70) {
        feedback += '<li>Review verb conjugation patterns for regular verbs</li>';
        feedback += '<li>Focus on one tense at a time before moving to others</li>';
    }
    
    const hasSubjunctiveErrors = sessionData.tenseErrors['presente subjuntivo'] || sessionData.tenseErrors['imperfecto subjuntivo'];
    if (hasSubjunctiveErrors) {
        feedback += '<li>Practice subjunctive mood - remember the "opposite vowel" rule</li>';
    }
    
    const hasIdentifyErrors = sessionData.questionTypeErrors['identify-tense'] || sessionData.questionTypeErrors['identify-pronoun'];
    if (hasIdentifyErrors) {
        feedback += '<li>Study verb endings to better identify tenses and pronouns</li>';
    }
    
    feedback += '<li>Take your time reading each question carefully</li>';
    feedback += '<li>Pay attention to the hints provided after wrong answers</li>';
    feedback += '</ul></div>';
    
    return feedback;
}

function closeSessionSummary() {
    document.getElementById('session-summary-modal').style.display = 'none';
    sessionActive = false;
    document.getElementById('session-panel').style.display = 'block';
    document.getElementById('session-progress').style.display = 'none';
}

function restartSession() {
    closeSessionSummary();
    startSession();
}

// Event listeners
nextBtnEl.addEventListener('click', loadQuestion);

// Initialize
loadBestStreak();
loadQuestion();

// Add keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && nextBtnEl.style.display !== 'none') {
        loadQuestion();
    }
    
    // Number keys for quick answer selection
    if (!isAnswered && e.key >= '1' && e.key <= '4') {
        const index = parseInt(e.key) - 1;
        const buttons = document.querySelectorAll('.option-btn');
        if (buttons[index]) {
            buttons[index].click();
        }
    }
});
