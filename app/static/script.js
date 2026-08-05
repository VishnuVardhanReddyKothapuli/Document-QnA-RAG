document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const uploadSection = document.getElementById('uploadSection');
    const chatSection = document.getElementById('chatSection');
    const uploadStatus = document.getElementById('uploadStatus');
    const chatForm = document.getElementById('chatForm');
    const questionInput = document.getElementById('questionInput');
    const chatHistory = document.getElementById('chatHistory');
    const sendBtn = document.getElementById('sendBtn');

    // --- File Upload Logic ---
    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileUpload(fileInput.files[0]);
        }
    });

    async function handleFileUpload(file) {
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showUploadStatus('Please upload a valid PDF file.', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        showUploadStatus('Processing PDF, please wait...', 'loading');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (response.ok) {
                showUploadStatus(data.message, 'success');
                setTimeout(() => {
                    uploadSection.classList.add('hidden');
                    chatSection.classList.remove('hidden');
                    questionInput.focus();
                }, 1500);
            } else {
                showUploadStatus(data.detail || 'An error occurred during upload.', 'error');
            }
        } catch (error) {
            showUploadStatus('Network error. Please try again.', 'error');
        }
    }

    function showUploadStatus(message, type) {
        uploadStatus.textContent = message;
        uploadStatus.className = `status-message ${type}`;
        uploadStatus.classList.remove('hidden');
    }

    // --- Chat Logic ---
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = questionInput.value.trim();
        if (!question) return;

        appendMessage('user', question);
        questionInput.value = '';
        sendBtn.disabled = true;

        const loadingId = appendLoadingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question })
            });
            
            removeElement(loadingId);
            
            const data = await response.json();
            
            if (response.ok) {
                appendMessage('system', data.response);
            } else {
                appendMessage('system', `Error: ${data.detail || 'Failed to get a response.'}`);
            }
        } catch (error) {
            removeElement(loadingId);
            appendMessage('system', 'Network error. Please try again.');
        } finally {
            sendBtn.disabled = false;
            questionInput.focus();
        }
    });

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        // Very simple markdown formatting for newlines and bold (if needed)
        let formattedText = text.replace(/\n/g, '<br>');
        bubble.innerHTML = formattedText;
        
        messageDiv.appendChild(bubble);
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }

    function appendLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.id = id;
        messageDiv.className = `message system-message`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.innerHTML = `
            <div class="loading-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        
        messageDiv.appendChild(bubble);
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});
