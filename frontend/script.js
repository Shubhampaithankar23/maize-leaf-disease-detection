/* ============================================
   SMART MAIZE LEAF DISEASE DETECTION SYSTEM
   Frontend JavaScript - Main Application Logic
   ============================================ */

// Configuration
const CONFIG = {
    API_URL: 'http://localhost:8000',
    MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
    ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
};

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const uploadBtn = document.getElementById('uploadBtn');
const clearBtn = document.getElementById('clearBtn');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const logoutBtn = document.getElementById('logoutBtn');
const userName = document.getElementById('userName');

// State
let selectedFile = null;
let isAnalyzing = false;

// ============================================
// AUTHENTICATION
// ============================================

function checkAuthentication() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (!isLoggedIn) {
        window.location.href = 'login.html';
    }
}

function displayUsername() {
    const username = localStorage.getItem('currentUser');
    if (userName && username) {
        userName.textContent = username;
    }
}

function logout() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('currentUser');
    window.location.href = 'login.html';
}

// Check auth on page load
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    displayUsername();
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
});

// ============================================
// UPLOAD HANDLING
// ============================================

uploadBtn.addEventListener('click', () => {
    imageInput.click();
});

imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

clearBtn.addEventListener('click', clearSelection);

// ============================================
// FILE HANDLING
// ============================================

function handleFileSelect(file) {
    // Validation
    if (!CONFIG.ALLOWED_TYPES.includes(file.type)) {
        showError('Please upload a valid image file (JPEG, PNG, WebP)');
        return;
    }

    if (file.size > CONFIG.MAX_FILE_SIZE) {
        showError('File size exceeds 10MB limit');
        return;
    }

    selectedFile = file;
    hideError();

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
        uploadArea.style.display = 'none';
        uploadBtn.style.display = 'none';

        // Auto-analyze after preview
        setTimeout(() => {
            analyzeImage();
        }, 500);
    };
    reader.readAsDataURL(file);
}

function clearSelection() {
    selectedFile = null;
    imageInput.value = '';
    previewContainer.style.display = 'none';
    uploadArea.style.display = 'block';
    uploadBtn.style.display = 'block';
    resultsSection.style.display = 'none';
    hideError();
}

// ============================================
// IMAGE ANALYSIS
// ============================================

async function analyzeImage() {
    if (!selectedFile) {
        showError('Please select an image first');
        return;
    }

    // Prevent multiple simultaneous requests
    if (isAnalyzing) {
        return;
    }

    isAnalyzing = true;

    try {
        // Show loading spinner
        loadingSpinner.style.display = 'flex';
        resultsSection.style.display = 'none';
        hideError();

        // Prepare form data
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Start timer
        const startTime = performance.now();

        // Send request
        const response = await fetch(`${CONFIG.API_URL}/api/predict`, {
            method: 'POST',
            body: formData
        });

        const endTime = performance.now();
        const processingTime = ((endTime - startTime) / 1000).toFixed(2);

        // Hide loading spinner FIRST
        loadingSpinner.style.display = 'none';

        if (!response.ok) {
            const errorText = await response.text();
            try {
                const errorData = JSON.parse(errorText);
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            } catch (e) {
                throw new Error(`Server error: ${response.status}`);
            }
        }

        const data = await response.json();

        // Display results
        displayResults(data, processingTime);

    } catch (error) {
        loadingSpinner.style.display = 'none';
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        isAnalyzing = false;
    }
}

// ============================================
// RESULTS DISPLAY
// ============================================

function displayResults(data, processingTime) {
    // Update prediction card
    document.getElementById('diseaseName').textContent = data.disease || 'Unknown';
    const confidence = Math.round((data.confidence || 0) * 100);
    document.getElementById('confidenceScore').textContent = `${confidence}%`;
    
    const confidenceFill = document.getElementById('confidenceFill');
    confidenceFill.style.width = `${confidence}%`;
    document.getElementById('confidenceText').textContent = `${confidence}%`;
    
    document.getElementById('detectionTime').textContent = `${processingTime}s`;

    // Update explainability section
    if (data.heatmap) {
        document.getElementById('heatmapImage').src = `${CONFIG.API_URL}/${data.heatmap}`;
        document.getElementById('heatmapImage').style.display = 'block';
        document.getElementById('heatmapPlaceholder').style.display = 'none';
    } else {
        document.getElementById('heatmapImage').style.display = 'none';
        document.getElementById('heatmapPlaceholder').style.display = 'block';
    }

    // Update recommendations - preserve line breaks
    const recommendation = data.recommendation || {};
    
    // Use textContent for security, but handle newlines
    const setCellContent = (id, text) => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = text || '-';
            // Preserve whitespace
            element.style.whiteSpace = 'pre-wrap';
        }
    };
    
    setCellContent('diseaseCause', recommendation.cause || '-');
    setCellContent('pesticide', recommendation.pesticide || '-');
    setCellContent('fertilizer', recommendation.fertilizer || '-');
    setCellContent('prevention', recommendation.prevention || '-');

    // Show results section with animation
    resultsSection.style.display = 'block';
    window.scrollTo({ top: resultsSection.offsetTop - 100, behavior: 'smooth' });
}

// ============================================
// ERROR HANDLING
// ============================================

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'flex';
}

function hideError() {
    errorMessage.style.display = 'none';
}

// ============================================
// ACCESSIBILITY & KEYBOARD SUPPORT
// ============================================

document.addEventListener('keydown', (e) => {
    // Press 'C' to clear selection
    if (e.key === 'c' || e.key === 'C') {
        if (previewContainer.style.display === 'block') {
            clearSelection();
        }
    }
});

// ============================================
// RESPONSIVE BEHAVIOR
// ============================================

window.addEventListener('resize', () => {
    // Adjust layout if needed
    const width = window.innerWidth;
    if (width < 768) {
        // Mobile-specific adjustments
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Smart Maize Leaf Disease Detection System - Ready');

    // Test backend connectivity
    testBackendConnection();
});

async function testBackendConnection() {
    try {
        console.log('Testing backend connection to:', CONFIG.API_URL);
        const response = await fetch(`${CONFIG.API_URL}/api/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend connection successful:', data);
        } else {
            console.error('❌ Backend connection failed:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('❌ Backend connection error:', error.message);
        console.error('Full error:', error);
    }
}

// ============================================
// UTILITY FUNCTIONS
// ============================================

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function getCurrentTimestamp() {
    const now = new Date();
    return now.toLocaleString();
}
