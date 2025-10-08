document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const centralContent = document.getElementById('centralContent');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarToggleMobile = document.getElementById('sidebarToggleMobile');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.getElementById('uploadForm');
    const uploadDefault = document.getElementById('uploadDefault');
    const uploadPreview = document.getElementById('uploadPreview');
    const previewImage = document.getElementById('previewImage');
    const imageInfo = document.getElementById('imageInfo');
    const modelChoice = document.getElementById('modelChoice');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const changeImageBtn = document.getElementById('changeImageBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const predictionResultsContainer = document.getElementById('predictionResultsContainer');
    const predictionResults = document.getElementById('predictionResults');
    const resultsContent = document.getElementById('resultsContent');
    const selectedModelName = document.getElementById('selectedModelName');
    const cancelAnalysisBtn = document.getElementById('cancelAnalysisBtn');
    const closeResultsBtn = document.getElementById('closeResultsBtn');
    const modelDropdownBtn = document.getElementById('modelDropdownBtn');
    const modelDropdown = document.getElementById('modelDropdown');
    const currentModel = document.getElementById('currentModel');
    const historyItemsContainer = document.getElementById('historyItems');
    const historyItems = document.querySelectorAll('.history-item');
    
    // Model selection
    const modelOptions = document.querySelectorAll('.model-option');
    let currentAnalysisRequest = null;
    let isSidebarCollapsed = false;
    let currentPredictionData = null; // Store current prediction data

    // Initialize the application
    initializeApp();

    function initializeApp() {
        // Set CNN as default
        setSelectedModel('cnn_model');
        
        // Set up all event listeners
        setupEventListeners();
        
        // Ensure upload section is visible initially
        showUploadSection();
    }

    function setupEventListeners() {
        // Sidebar toggle functionality
        sidebarToggle.addEventListener('click', function() {
            isSidebarCollapsed = !isSidebarCollapsed;
            sidebar.classList.toggle('collapsed', isSidebarCollapsed);
            
            // Update toggle icon
            const icon = this.querySelector('i');
            icon.className = isSidebarCollapsed ? 'fas fa-chevron-right' : 'fas fa-chevron-left';
        });

        sidebarToggleMobile.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });

        // Model dropdown functionality
        modelDropdownBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            modelDropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function() {
            modelDropdown.classList.remove('show');
        });

        modelDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        // Model selection handlers
        modelOptions.forEach(option => {
            option.addEventListener('click', function() {
                const modelId = this.dataset.modelId;
                const modelName = this.dataset.modelName;
                setSelectedModel(modelId);
                currentModel.textContent = modelName;
                modelDropdown.classList.remove('show');
            });
        });

        // History item click handlers - FIXED: Load data directly without loading message
        historyItems.forEach(item => {
            item.addEventListener('click', function() {
                const historyId = this.dataset.historyId;
                const predictedClass = this.querySelector('.history-class').textContent;
                const modelUsed = this.querySelector('.history-model').textContent;
                const confidence = this.querySelector('.history-confidence').textContent;
                const timestamp = this.querySelector('.history-time').textContent;
                
                loadHistoryResult(historyId, predictedClass, modelUsed, confidence, timestamp);
            });
        });

        // File input handler
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validate file size (10MB max)
                if (file.size > 10 * 1024 * 1024) {
                    alert('File size must be less than 10MB');
                    fileInput.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    
                    // Show image info
                    const fileSize = (file.size / 1024 / 1024).toFixed(2);
                    imageInfo.innerHTML = `
                        <div><strong>File:</strong> ${file.name}</div>
                        <div><strong>Size:</strong> ${fileSize} MB</div>
                        <div><strong>Type:</strong> ${file.type}</div>
                    `;
                    
                    // Switch to preview state
                    showImagePreview();
                };
                reader.readAsDataURL(file);
            }
        });

        // Change image button
        changeImageBtn.addEventListener('click', function() {
            resetToUploadState();
        });

        // Analyze button
        analyzeBtn.addEventListener('click', function() {
            if (!fileInput.files[0]) {
                alert('Please select an image file first.');
                return;
            }

            startAnalysis();
        });

        // Cancel analysis button
        cancelAnalysisBtn.addEventListener('click', function() {
            if (currentAnalysisRequest) {
                currentAnalysisRequest.abort();
                currentAnalysisRequest = null;
            }
            resetToUploadState();
        });

        // Close results button - UPDATED: Now adds to recent history and updates
        closeResultsBtn.addEventListener('click', function() {
            // If we have current prediction data, add it to recent history
            if (currentPredictionData) {
                addToRecentHistory(currentPredictionData);
            } else {
                // If no current data, still refresh to show any updates
                refreshRecentActivities();
            }
            
            resetToUploadState();
        });
    }

    function setSelectedModel(modelId) {
        // Update radio buttons
        modelOptions.forEach(option => {
            const radio = option.querySelector('input[type="radio"]');
            if (radio.value === modelId) {
                option.classList.add('selected');
                radio.checked = true;
            } else {
                option.classList.remove('selected');
                radio.checked = false;
            }
        });
        
        // Update hidden input
        modelChoice.value = modelId;
        
        // Update model name for display
        const selectedOption = Array.from(modelOptions).find(opt => opt.dataset.modelId === modelId);
        if (selectedOption) {
            selectedModelName.textContent = selectedOption.dataset.modelName;
        }
    }

    function showUploadSection() {
        // Show the main upload section and hide everything else
        uploadDefault.style.display = 'block';
        uploadPreview.style.display = 'none';
        loadingIndicator.style.display = 'none';
        hidePredictionResults();
    }

    function showImagePreview() {
        // Show image preview and hide upload default
        uploadDefault.style.display = 'none';
        uploadPreview.style.display = 'block';
        loadingIndicator.style.display = 'none';
        hidePredictionResults();
    }

    function showLoadingIndicator() {
        // Show loading and hide everything else
        uploadDefault.style.display = 'none';
        uploadPreview.style.display = 'none';
        loadingIndicator.style.display = 'block';
        hidePredictionResults();
    }

    function showPredictionResults() {
        // Show prediction results - everything else remains as is
        predictionResultsContainer.style.display = 'block';
        predictionResults.style.display = 'block';
    }

    function hidePredictionResults() {
        // Hide prediction results only
        predictionResultsContainer.style.display = 'none';
        predictionResults.style.display = 'none';
    }

    function resetToUploadState() {
        // Reset everything to initial upload state
        if (currentAnalysisRequest) {
            currentAnalysisRequest.abort();
            currentAnalysisRequest = null;
        }
        
        fileInput.value = '';
        showUploadSection();
        
        // Clear current prediction data
        currentPredictionData = null;
    }

    function startAnalysis() {
        // Show loading indicator
        showLoadingIndicator();

        // Submit form via AJAX
        const formData = new FormData(uploadForm);
        
        // Create abort controller for cancellation
        const controller = new AbortController();
        currentAnalysisRequest = controller;

        fetch(uploadForm.action, {
            method: 'POST',
            body: formData,
            signal: controller.signal,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
                resetToUploadState();
            } else {
                // Store the prediction data for potential saving later
                currentPredictionData = {
                    predictedClass: data.prediction.class_name,
                    confidence: data.prediction.confidence,
                    modelUsed: data.prediction.model_used,
                    imageUrl: data.image.url,
                    description: data.prediction.description,
                    riskLevel: data.prediction.risk_level,
                    recommendation: data.prediction.recommendation
                };
                
                displayPredictionResults(data);
            }
        })
        .catch(error => {
            if (error.name !== 'AbortError') {
                console.error('Error:', error);
                alert('An error occurred during analysis.');
                resetToUploadState();
            }
        })
        .finally(() => {
            loadingIndicator.style.display = 'none';
            currentAnalysisRequest = null;
        });
    }

    // FIXED: Load history data directly without loading message
    function loadHistoryResult(historyId, predictedClass, modelUsed, confidence, timestamp) {
        // For demo purposes, we'll create sample data based on the history item
        // In a real application, you would fetch this data from your server
        
        const sampleData = {
            image: {
                url: '/media/uploads/sample_history_image.jpg', // This would be the actual image URL from your database
                name: 'History Analysis',
                size: 2048576 // Sample file size
            },
            prediction: {
                class_name: predictedClass,
                confidence: parseFloat(confidence),
                model_used: modelUsed,
                description: getConditionDescription(predictedClass),
                risk_level: getRiskLevel(predictedClass),
                recommendation: getRecommendation(predictedClass),
                timestamp: new Date().toLocaleString() // Use actual timestamp from database
            }
        };
        
        displayPredictionResults(sampleData);
    }

    // SIMPLIFIED: Only two classes now
    function getConditionDescription(condition) {
        const descriptions = {
            'Normal (no stone)': 'No kidney stones detected. The kidney appears healthy and normal.',
            'Stone': 'Kidney stone detected. Further medical evaluation recommended.'
        };
        return descriptions[condition] || 'Kidney analysis completed.';
    }

    function getRiskLevel(condition) {
        const riskLevels = {
            'Normal (no stone)': 'Low',
            'Stone': 'Medium-High'
        };
        return riskLevels[condition] || 'Unknown';
    }

    function getRecommendation(condition) {
        const recommendations = {
            'Normal (no stone)': 'Maintain regular checkups and healthy hydration. Continue with routine kidney health monitoring.',
            'Stone': 'Consult with a urologist for proper diagnosis and treatment plan. Increase fluid intake and follow medical advice.'
        };
        return recommendations[condition] || 'Consult healthcare professional for proper diagnosis.';
    }

    // NEW FUNCTION: Refresh recent activities section
    function refreshRecentActivities() {
        fetch('/classification/refresh-history/')
            .then(response => response.json())
            .then(data => {
                // Update the history items container with new HTML
                if (historyItemsContainer && data.history_html) {
                    historyItemsContainer.innerHTML = data.history_html;
                    
                    // Re-attach click event listeners to the new history items
                    const newHistoryItems = document.querySelectorAll('.history-item');
                    newHistoryItems.forEach(item => {
                        item.addEventListener('click', function() {
                            const historyId = this.dataset.historyId;
                            const predictedClass = this.querySelector('.history-class').textContent;
                            const modelUsed = this.querySelector('.history-model').textContent;
                            const confidence = this.querySelector('.history-confidence').textContent;
                            const timestamp = this.querySelector('.history-time').textContent;
                            
                            loadHistoryResult(historyId, predictedClass, modelUsed, confidence, timestamp);
                        });
                    });
                }
            })
            .catch(error => {
                console.log('Could not refresh recent activities:', error);
            });
    }

    // NEW FUNCTION: Add current analysis to recent history
    function addToRecentHistory(predictionData) {
        // Make an API call to save this analysis to the database
        fetch('/classification/save-history/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                predicted_class: predictionData.predictedClass,
                confidence: predictionData.confidence,
                model_used: predictionData.modelUsed,
                image_url: predictionData.imageUrl,
                description: predictionData.description,
                risk_level: predictionData.riskLevel,
                recommendation: predictionData.recommendation
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Analysis saved to history');
                // Refresh the recent activities to show the new entry
                refreshRecentActivities();
            } else {
                console.error('Failed to save history:', data.message);
                // Still refresh to show any other updates
                refreshRecentActivities();
            }
        })
        .catch(error => {
            console.error('Error saving to history:', error);
            // Even if save fails, still refresh to show any other updates
            refreshRecentActivities();
        });
    }

    // NEW FUNCTION: Get CSRF token for Django (required for POST requests)
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfToken ? csrfToken.value : '';
    }

    function displayPredictionResults(data) {
        const prediction = data.prediction;
        const image = data.image;
        
        let confidenceClass = 'confidence-high';
        if (prediction.confidence < 70) confidenceClass = 'confidence-medium';
        if (prediction.confidence < 50) confidenceClass = 'confidence-low';
        
        let riskClass = 'risk-low';
        if (prediction.risk_level.includes('Medium')) riskClass = 'risk-medium';
        if (prediction.risk_level.includes('High')) riskClass = 'risk-high';
        
        resultsContent.innerHTML = `
            <div class="report-section">
                <h4><i class="fas fa-image"></i> Uploaded Image</h4>
                <div class="prediction-image">
                    <img src="${image.url}" alt="Analyzed Kidney Stone Image" onerror="this.style.display='none'">
                    <div style="margin-top: 15px; color: #718096; font-size: 0.9em;">
                        <strong>File:</strong> ${image.name} 
                        ${image.size ? `| <strong>Size:</strong> ${(image.size / 1024 / 1024).toFixed(2)} MB` : ''}
                    </div>
                </div>
            </div>
            
            <div class="report-section">
                <h4><i class="fas fa-diagnoses"></i> Diagnosis Summary</h4>
                <div class="report-grid">
                    <div class="report-item">
                        <strong>Predicted Condition</strong>
                        <div style="font-size: 1.3em; font-weight: bold; color: #2d3748; margin-top: 8px;">
                            ${prediction.class_name}
                        </div>
                    </div>
                    <div class="report-item">
                        <strong>Confidence Level</strong>
                        <div class="${confidenceClass}" style="margin-top: 8px;">
                            ${prediction.confidence}%
                        </div>
                    </div>
                    <div class="report-item">
                        <strong>Risk Assessment</strong>
                        <div class="${riskClass}" style="margin-top: 8px; font-weight: bold;">
                            ${prediction.risk_level}
                        </div>
                    </div>
                    <div class="report-item">
                        <strong>AI Model Used</strong>
                        <div style="margin-top: 8px; color: #3182ce; font-weight: 600;">
                            ${prediction.model_used}
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="report-section">
                <h4><i class="fas fa-info-circle"></i> Condition Description</h4>
                <p style="font-size: 1.1em; line-height: 1.6; color: #4a5568;">${prediction.description}</p>
            </div>
            
            <div class="report-section">
                <h4><i class="fas fa-stethoscope"></i> Medical Recommendation</h4>
                <div class="recommendation-box">
                    <strong>Recommended Action:</strong>
                    <p style="margin-top: 12px; margin-bottom: 0; font-size: 1.1em; line-height: 1.6;">
                        ${prediction.recommendation}
                    </p>
                </div>
            </div>
        `;
        
        // Store the current prediction data for potential saving
        if (!currentPredictionData) {
            currentPredictionData = {
                predictedClass: prediction.class_name,
                confidence: prediction.confidence,
                modelUsed: prediction.model_used,
                imageUrl: image.url,
                description: prediction.description,
                riskLevel: prediction.risk_level,
                recommendation: prediction.recommendation
            };
        }
        
        // Show prediction results
        showPredictionResults();
        
        // Scroll to results
        predictionResults.scrollIntoView({ behavior: 'smooth' });
    }
});