// Game state
let currentQuestion = null;
let score = 0;
let streak = 0;
let bestStreak = 0;
let questionsAnswered = 0;
let isAnswered = false;

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

// Load a new question
async function loadQuestion() {
    try {
        const response = await fetch('/api/question');
        currentQuestion = await response.json();
        
        // Update UI based on question type
        infinitiveEl.textContent = currentQuestion.verb;
        englishEl.textContent = currentQuestion.english;
        
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
                tense: currentQuestion.tense
            })
        });
        const result = await response.json();
        
        // Update button styling
        if (isCorrect) {
            button.classList.add('correct');
            showFeedback(true, result);
            updateScore(true);
            playSound('correct');
        } else {
            button.classList.add('incorrect');
            showFeedback(false, result);
            updateScore(false);
            playSound('incorrect');
            
            // Highlight correct answer
            allButtons.forEach(btn => {
                if (btn.textContent === currentQuestion.correct_answer) {
                    btn.classList.add('correct');
                }
            });
        }
    } catch (error) {
        console.error('Error checking answer:', error);
        // Fallback to local check
        if (isCorrect) {
            button.classList.add('correct');
            showFeedback(true, {});
            updateScore(true);
            playSound('correct');
        } else {
            button.classList.add('incorrect');
            showFeedback(false, {});
            updateScore(false);
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
        if (currentQuestion.question_type === 'identify-tense') {
            message += ` Correct tense: ${currentQuestion.correct_answer}`;
        } else if (currentQuestion.question_type === 'identify-pronoun') {
            message += ` Correct pronoun: ${currentQuestion.correct_answer}`;
        } else {
            message += ` Correct answer: ${currentQuestion.correct_answer}`;
        }
    }
    
    // Add tense description if available
    if (result.tense_description && result.tense_name) {
        message += `\n\n${result.tense_name}: ${result.tense_description}`;
    }
    
    feedbackEl.textContent = message;
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
    const progress = (questionsAnswered % 10) * 10;
    progressBarEl.style.width = progress + '%';
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
