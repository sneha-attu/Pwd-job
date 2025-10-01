// Speech and Voice Features for PWD Job Portal

class SpeechController {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.recognition = null;
        this.isListening = false;
        this.isReading = false;
        
        this.initializeSpeechFeatures();
    }
    
    initializeSpeechFeatures() {
        // Text-to-speech button
        document.getElementById('text-to-speech')?.addEventListener('click', () => this.toggleTextToSpeech());
        
        // Voice navigation button  
        document.getElementById('voice-navigation')?.addEventListener('click', () => this.toggleVoiceNavigation());
        
        // Initialize speech recognition if available
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.setupSpeechRecognition();
        }
    }
    
    toggleTextToSpeech() {
        if (this.isReading) {
            this.stopReading();
        } else {
            this.startReading();
        }
    }
    
    startReading() {
        const content = this.getPageContent();
        if (content) {
            const utterance = new SpeechSynthesisUtterance(content);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            
            utterance.onstart = () => {
                this.isReading = true;
                this.updateTTSButton('Reading...', 'btn-warning');
            };
            
            utterance.onend = () => {
                this.isReading = false;
                this.updateTTSButton('Read Aloud', 'btn-outline-light');
            };
            
            this.synthesis.speak(utterance);
        }
    }
    
    stopReading() {
        this.synthesis.cancel();
        this.isReading = false;
        this.updateTTSButton('Read Aloud', 'btn-outline-light');
    }
    
    getPageContent() {
        const main = document.getElementById('main-content');
        if (!main) return '';
        
        // Get text content excluding buttons and navigation
        const textElements = main.querySelectorAll('h1, h2, h3, h4, h5, h6, p, li');
        let content = '';
        
        textElements.forEach(el => {
            content += el.textContent.trim() + '. ';
        });
        
        return content;
    }
    
    updateTTSButton(text, className) {
        const button = document.getElementById('text-to-speech');
        if (button) {
            button.innerHTML = `<i class="fas fa-volume-up"></i> ${text}`;
            button.className = `btn btn-sm ${className}`;
        }
    }
    
    toggleVoiceNavigation() {
        if (this.isListening) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }
    
    setupSpeechRecognition() {
        if (!this.recognition) return;
        
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';
        
        this.recognition.onresult = (event) => {
            const command = event.results[0][0].transcript.toLowerCase();
            this.processVoiceCommand(command);
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            this.updateVoiceButton('Voice Nav', 'btn-outline-light');
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateVoiceButton('Voice Nav', 'btn-outline-light');
        };
    }
    
    startListening() {
        if (this.recognition && !this.isListening) {
            this.recognition.start();
            this.isListening = true;
            this.updateVoiceButton('Listening...', 'btn-danger');
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
            this.isListening = false;
            this.updateVoiceButton('Voice Nav', 'btn-outline-light');
        }
    }
    
    updateVoiceButton(text, className) {
        const button = document.getElementById('voice-navigation');
        if (button) {
            button.innerHTML = `<i class="fas fa-microphone"></i> ${text}`;
            button.className = `btn btn-sm ${className}`;
        }
    }
    
    processVoiceCommand(command) {
        console.log('Voice command:', command);
        
        if (command.includes('home')) {
            window.location.href = '/';
        } else if (command.includes('jobs') || command.includes('job')) {
            window.location.href = '/jobs';
        } else if (command.includes('login') || command.includes('sign in')) {
            window.location.href = '/login';
        } else if (command.includes('register') || command.includes('sign up')) {
            window.location.href = '/register';
        } else if (command.includes('profile')) {
            window.location.href = '/profile';
        } else if (command.includes('search')) {
            const searchInput = document.getElementById('job-search');
            if (searchInput) {
                searchInput.focus();
            }
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SpeechController();
});
