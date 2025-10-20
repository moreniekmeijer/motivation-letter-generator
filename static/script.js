const DAILY_LIMIT = 3;

const generateBtn = document.getElementById('generate-btn');
const loadingSpinner = document.getElementById('loading-spinner');
const generateForm = document.getElementById('generate-form');

function getGenerationsToday() {
    const today = new Date().toLocaleDateString();
    const generations = JSON.parse(localStorage.getItem('generations') || '{}');

    Object.keys(generations).forEach(date => {
        if (date !== today) delete generations[date];
    });

    localStorage.setItem('generations', JSON.stringify(generations));
    return generations[today] || 0;
}

function incrementGenerations() {
    const today = new Date().toLocaleDateString();
    const generations = JSON.parse(localStorage.getItem('generations') || '{}');
    generations[today] = (generations[today] || 0) + 1;
    localStorage.setItem('generations', JSON.stringify(generations));
}

function updateGenerationLimit() {
    const todayCount = getGenerationsToday();
    const remaining = DAILY_LIMIT - todayCount;
    const limitDiv = document.getElementById('generation-limit');

    limitDiv.textContent = `You have ${remaining} letter generation${remaining === 1 ? '' : 's'} remaining today.`;
    limitDiv.className = remaining === 0 ? 'limit-warning' : '';

    generateBtn.disabled = remaining === 0;
}

function handleFormSubmit(event) {
    const todayCount = getGenerationsToday();

    if (todayCount >= DAILY_LIMIT) {
        event.preventDefault();
        alert(`You have reached your daily limit of ${DAILY_LIMIT} generations. Please try again tomorrow.`);
        return;
    }

    generateBtn.classList.add('hidden');
    loadingSpinner.classList.remove('hidden');

    incrementGenerations();
    updateGenerationLimit();
}

function resetFormUI() {
    generateBtn.classList.remove('hidden');
    loadingSpinner.classList.add('hidden');
    generateBtn.disabled = false;
}

function loadHistory() {
    const container = document.getElementById('history');
    const history = JSON.parse(localStorage.getItem('letters') || '[]');

    if (history.length === 0) {
        container.innerHTML = '<p>No letters yet. Generate one above!</p>';
        return;
    }

    container.innerHTML = '';
    history.forEach((letter, index) => {
        const div = document.createElement('div');
        div.className = 'letter-box';
        div.innerHTML = `
            <h3>${escapeHtml(letter.title)}</h3>
            <p class="meta">Created: ${new Date(letter.created_at).toLocaleString()}</p>
            <div class="letter-actions">
                <button onclick="downloadFromHistory(${index})">Download</button>
                <button onclick="deleteLetter(${index})" class="delete-btn">Delete</button>
            </div>
        `;
        container.appendChild(div);
    });
}

function downloadFromHistory(index) {
    const letters = JSON.parse(localStorage.getItem('letters') || '[]');
    const letter = letters[index];
    if (!letter) return;

    const blob = new Blob([letter.content], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = letter.title.replace(/\s+/g, '_') + '.txt';
    a.click();
    URL.revokeObjectURL(a.href);
}

function deleteLetter(index) {
    if (!confirm('Are you sure you want to delete this letter?')) return;

    const history = JSON.parse(localStorage.getItem('letters') || '[]');
    history.splice(index, 1);
    localStorage.setItem('letters', JSON.stringify(history));
    loadHistory();
}

function saveNewLetter(title, content) {
    try {
        const history = JSON.parse(localStorage.getItem('letters') || '[]');
        const newLetter = {
            title: title,
            content: content,
            created_at: new Date().toISOString()
        };

        history.unshift(newLetter);
        localStorage.setItem('letters', JSON.stringify(history));

        const blob = new Blob([content], { type: 'text/plain' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = title.replace(/\s+/g, '_') + '.txt';
        a.click();
        URL.revokeObjectURL(a.href);

        loadHistory();
    } catch (error) {
        console.error('Error saving letter:', error);
        alert('Failed to save letter. Please try again.');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function initializeEventListeners() {
    generateForm.addEventListener('submit', handleFormSubmit);

    window.addEventListener('pageshow', resetFormUI);
}

function initialize() {
    loadHistory();
    updateGenerationLimit();
    initializeEventListeners();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}