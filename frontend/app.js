// ==========================
// Frontend interactions (chat + image prediction)
// Improved: loading state, markdown rendering, safe UI messages, chat-bubble styling
// ==========================

const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const predictBtn = document.getElementById("predictBtn");
const diseaseName = document.getElementById("disease");
const confidence = document.getElementById("confidence");
const description = document.getElementById("description");
const progressBar = document.getElementById("progressBar");

const askBtn = document.getElementById("askBtn");
const answerContainer = document.getElementById("answer");
const questionInput = document.getElementById("question");

const API_URL = "http://127.0.0.1:8003";

// Simple markdown-to-HTML renderer (supports headings, bold, italics, code blocks, lists, links)
function renderMarkdown(md) {
    if (!md) return '';
    // Escape HTML special chars
    let s = md.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Code blocks ```
    s = s.replace(/```([\s\S]*?)```/g, function(m, code) {
        return '<pre class="code">' + code.replace(/&lt;/g,'<').replace(/&gt;/g,'>') + '</pre>';
    });
    // Inline code `code`
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Headings
    s = s.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    s = s.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    s = s.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold **text**
    s = s.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    // Italic *text*
    s = s.replace(/\*(.*?)\*/gim, '<em>$1</em>');

    // Links [text](url)
    s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Unordered lists
    s = s.replace(/^\s*[-\*] (.*)/gim, '<li>$1</li>');
    s = s.replace(/(<li>[\s\S]*?<\/li>)(?![\s\S]*<li>)/g, function(m){
        // wrap contiguous lis into ul
        return '<ul>' + m + '</ul>';
    });

    // Paragraphs
    s = s.replace(/^(?!<h|<ul|<pre|<li|<code|<blockquote)(.+)$/gim, '<p>$1</p>');

    return s;
}

function ensureStyles() {
    if (document.getElementById('rag-styles')) return;
    const style = document.createElement('style');
    style.id = 'rag-styles';
    style.innerHTML = `
    .chat-bubble { max-width: 760px; margin: 12px 0; padding: 12px 16px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); font-family: Inter, Roboto, Arial, sans-serif; }
    .chat-bubble.user { background: #e6f3ff; align-self: flex-end; }
    .chat-bubble.agent { background: #fff; border: 1px solid #eee; }
    .chat-container { display: flex; flex-direction: column; }
    pre.code { background:#0b0b0b; color:#f8f8f2; padding:10px; border-radius:6px; overflow:auto }
    code { background:#f4f4f4; padding:2px 4px; border-radius:4px; }
    `;
    document.head.appendChild(style);
}

ensureStyles();

askBtn.addEventListener('click', async () => {
    const question = questionInput.value || '';
    if (question.trim() === '') {
        alert('Please enter a question.');
        return;
    }

    // UI: set loading state
    askBtn.disabled = true;
    const prevText = askBtn.innerHTML;
    askBtn.innerHTML = 'Thinking...';

    // Show a temporary chat bubble for user question + loading agent bubble
    const container = document.createElement('div');
    container.className = 'chat-container';

    const userBubble = document.createElement('div');
    userBubble.className = 'chat-bubble user';
    userBubble.textContent = question;
    container.appendChild(userBubble);

    const agentBubble = document.createElement('div');
    agentBubble.className = 'chat-bubble agent';
    agentBubble.innerHTML = '<em>Thinking...</em>';
    container.appendChild(agentBubble);

    // Append to answer container (prepend so newest on bottom)
    answerContainer.prepend(container);

    try {
        const res = await fetch(`${API_URL}/shetimitra`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });

        if (!res.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await res.json();
        let text = data && data.answer ? data.answer : null;

        // If API returned a message with internal debug markers, replace it in UI unless DEBUG flag is set
        const DEBUG = (new URLSearchParams(window.location.search)).get('debug') === 'true';

        if (!text || typeof text !== 'string' || text.startsWith('[ERROR') || text.startsWith('[UNEXPECTED')) {
            // Show friendly message
            agentBubble.innerHTML = '<p>Sorry, I couldn\'t generate an answer. Please try again.</p>';
        } else {
            // Render markdown
            agentBubble.innerHTML = renderMarkdown(text);
        }

    } catch (err) {
        console.error('Chat error', err);
        // Friendly message
        const agentBubble = document.querySelector('.chat-bubble.agent');
        if (agentBubble) agentBubble.innerHTML = '<p>Sorry, I couldn\'t generate an answer. Please try again.</p>';
    } finally {
        // restore button state
        askBtn.disabled = false;
        askBtn.innerHTML = prevText;
    }
});

// ==========================
// Predict Button (unchanged)
// ==========================

predictBtn.addEventListener("click", async () => {
    const file = imageInput.files[0];
    if (!file) { alert("Please choose an image."); return; }

    predictBtn.innerHTML = "Predicting...";
    const result = await predictDisease(file);
    predictBtn.innerHTML = "Predict Disease";
    if (!result) return;

    const prediction = result[0];
    diseaseName.innerHTML = prediction.disease;
    confidence.innerHTML = prediction.confidence + "%";
    progressBar.style.width = prediction.confidence + "%";

    const info = diseaseData[prediction.disease];
    if (!info) { description.innerHTML = "No information available."; return; }

    description.innerHTML = `
        <h3>Description</h3>
        <p>${info.description}</p>
        <br>
        <h3>Symptoms</h3>
        <ul>
        ${info.symptoms.map(s => `<li>${s}</li>`).join("")}
        </ul>
        <br>
        <h3>Treatment</h3>
        <ul>
        ${info.treatment.map(s => `<li>${s}</li>`).join("")}
        </ul>
        <br>
        <h3>Prevention</h3>
        <ul>
        ${info.prevention.map(s => `<li>${s}</li>`).join("")}
        </ul>
    `;
    diseaseName.style.color = info.color;
});
