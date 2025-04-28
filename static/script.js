let questions = [];
let answers = [];
let currentIndex = 0;

async function startGame() {
    const res = await fetch('/start_game');
    const data = await res.json();
    questions = data.questions;
    currentIndex = 0;
    showQuestion();
}

function showQuestion() {
    if (currentIndex >= questions.length) {
        guessWord();
        return;
    }

    const questionElement = document.getElementById('question');
    questionElement.style.opacity = 0; // Fade out
    setTimeout(() => {
        questionElement.innerText = questions[currentIndex]; // Update question text
        questionElement.style.opacity = 1; // Fade in
    }, 500); // Wait for fade-out effect
}

async function submitAnswer(answer) {
    answers.push({ question: questions[currentIndex], answer: answer });
    currentIndex++;
    showQuestion();
}

async function guessWord() {
    const res = await fetch('/guess_word', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers: answers })
    });

    const resultDiv = document.getElementById('result');
    resultDiv.style.display = "block"; // Make result div visible

    if (res.ok) {
        const data = await res.json();
       resultDiv.innerHTML = `🧠 Are you thinking of: <b>${data.guess}</b>?<br>📚 Meaning: ${data.definition}`;
        resultDiv.classList.remove('error');
    } else {
        resultDiv.innerText = "😔 I couldn't guess! Please teach me later.";
        resultDiv.classList.add('error');
    }
}

// Start the game when the page loads
startGame();
