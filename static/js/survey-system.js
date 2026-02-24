// Post-Camp Survey System
class SurveyManager {
    constructor() {
        this.surveys = [];
        this.responses = [];
        this.init();
    }

    init() {
        this.addSurveyButton();
        this.setupSurveyModal();
    }

    addSurveyButton() {
        const campsSection = document.getElementById('camps');
        if (campsSection) {
            const header = campsSection.querySelector('h2');
            if (header) {
                const surveyButton = document.createElement('button');
                surveyButton.className = 'btn btn-success ms-3 coordinator-only admin-only organizer-only';
                surveyButton.innerHTML = '<i class="fas fa-poll me-2"></i>Post-Camp Surveys';
                surveyButton.onclick = () => this.showSurveyInterface();
                header.parentNode.appendChild(surveyButton);
            }
        }
    }

    setupSurveyModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'surveyModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-xl">
                <div class="modal-content modal-enhanced">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="fas fa-poll me-2"></i>Post-Camp Survey Management</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-4">
                                <h6><i class="fas fa-plus-circle me-2"></i>Create Survey</h6>
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <div class="mb-2">
                                            <input type="text" class="form-control form-control-sm" id="surveyTitle" placeholder="Survey Title">
                                        </div>
                                        <div class="mb-2">
                                            <select class="form-select form-select-sm" id="campForSurvey">
                                                <option value="">Select Camp</option>
                                            </select>
                                        </div>
                                        <div class="mb-2">
                                            <textarea class="form-control form-control-sm" id="surveyDescription" rows="2" placeholder="Survey Description"></textarea>
                                        </div>
                                        <button class="btn btn-primary btn-sm w-100" onclick="surveyManager.createSurvey()">
                                            <i class="fas fa-plus me-1"></i>Create Survey
                                        </button>
                                    </div>
                                </div>
                                
                                <h6><i class="fas fa-list me-2"></i>Active Surveys</h6>
                                <div id="surveysList" class="list-group">
                                    <!-- Surveys will be loaded here -->
                                </div>
                            </div>
                            <div class="col-md-8">
                                <h6><i class="fas fa-edit me-2"></i>Survey Builder</h6>
                                <div class="card">
                                    <div class="card-body">
                                        <div id="surveyBuilder">
                                            <p class="text-muted">Select a survey to edit or create a new one</p>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="mt-4">
                                    <h6><i class="fas fa-chart-bar me-2"></i>Survey Results</h6>
                                    <div class="card">
                                        <div class="card-body">
                                            <div id="surveyResults">
                                                <p class="text-muted">Select a survey to view results</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    async showSurveyInterface() {
        const modal = document.getElementById('surveyModal');
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        await this.loadCamps();
        await this.loadSurveys();
    }

    async loadCamps() {
        try {
            const response = await fetch('/api/camps');
            if (response.ok) {
                const camps = await response.json();
                const select = document.getElementById('campForSurvey');
                select.innerHTML = '<option value="">Select a camp...</option>';
                
                camps.forEach(camp => {
                    const option = document.createElement('option');
                    option.value = camp.id;
                    option.textContent = `${camp.name} - ${camp.type}`;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            toastManager.error('Failed to load camps');
        }
    }

    async loadSurveys() {
        try {
            const response = await fetch('/api/surveys');
            if (response.ok) {
                this.surveys = await response.json();
                this.renderSurveysList();
            }
        } catch (error) {
            toastManager.error('Failed to load surveys');
        }
    }

    renderSurveysList() {
        const listContainer = document.getElementById('surveysList');
        listContainer.innerHTML = '';
        
        this.surveys.forEach(survey => {
            const item = document.createElement('div');
            item.className = 'list-group-item list-group-item-action';
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="mb-1">${survey.title}</h6>
                        <small class="text-muted">${survey.camp_name} - ${survey.responses_count} responses</small>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="surveyManager.editSurvey(${survey.id})">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-success" onclick="surveyManager.viewResults(${survey.id})">
                            <i class="fas fa-chart-bar"></i>
                        </button>
                    </div>
                </div>
            `;
            listContainer.appendChild(item);
        });
    }

    async createSurvey() {
        const title = document.getElementById('surveyTitle').value;
        const campId = document.getElementById('campForSurvey').value;
        const description = document.getElementById('surveyDescription').value;
        
        if (!title || !campId) {
            toastManager.warning('Please fill all required fields');
            return;
        }
        
        try {
            const response = await fetch('/api/surveys', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, camp_id: campId, description })
            });
            
            if (response.ok) {
                toastManager.success('Survey created successfully');
                await this.loadSurveys();
                
                // Clear form
                document.getElementById('surveyTitle').value = '';
                document.getElementById('campForSurvey').value = '';
                document.getElementById('surveyDescription').value = '';
            }
        } catch (error) {
            toastManager.error('Failed to create survey');
        }
    }

    editSurvey(surveyId) {
        const survey = this.surveys.find(s => s.id === surveyId);
        if (!survey) return;
        
        this.renderSurveyBuilder(survey);
    }

    renderSurveyBuilder(survey) {
        const builder = document.getElementById('surveyBuilder');
        builder.innerHTML = `
            <div class="mb-3">
                <h6>${survey.title}</h6>
                <p class="text-muted">${survey.description}</p>
            </div>
            
            <div id="questionsContainer">
                ${survey.questions ? survey.questions.map((q, i) => this.renderQuestion(q, i)).join('') : ''}
            </div>
            
            <div class="mt-3">
                <button class="btn btn-outline-primary btn-sm" onclick="surveyManager.addQuestion()">
                    <i class="fas fa-plus me-1"></i>Add Question
                </button>
                <button class="btn btn-success btn-sm ms-2" onclick="surveyManager.saveSurvey(${survey.id})">
                    <i class="fas fa-save me-1"></i>Save Survey
                </button>
            </div>
        `;
    }

    renderQuestion(question, index) {
        return `
            <div class="card mb-3">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-8">
                            <input type="text" class="form-control form-control-sm mb-2" 
                                   placeholder="Question text" value="${question.text || ''}" 
                                   id="question_${index}">
                            <select class="form-select form-select-sm" id="question_type_${index}">
                                <option value="text" ${question.type === 'text' ? 'selected' : ''}>Text</option>
                                <option value="rating" ${question.type === 'rating' ? 'selected' : ''}>Rating (1-5)</option>
                                <option value="multiple" ${question.type === 'multiple' ? 'selected' : ''}>Multiple Choice</option>
                                <option value="yesno" ${question.type === 'yesno' ? 'selected' : ''}>Yes/No</option>
                            </select>
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-sm btn-outline-danger" onclick="surveyManager.removeQuestion(${index})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    addQuestion() {
        const container = document.getElementById('questionsContainer');
        const questionCount = container.children.length;
        
        const questionDiv = document.createElement('div');
        questionDiv.innerHTML = this.renderQuestion({ text: '', type: 'text' }, questionCount);
        container.appendChild(questionDiv.firstElementChild);
    }

    removeQuestion(index) {
        const container = document.getElementById('questionsContainer');
        if (container.children[index]) {
            container.children[index].remove();
        }
    }

    async saveSurvey(surveyId) {
        const questions = [];
        const container = document.getElementById('questionsContainer');
        
        for (let i = 0; i < container.children.length; i++) {
            const questionText = document.getElementById(`question_${i}`)?.value;
            const questionType = document.getElementById(`question_type_${i}`)?.value;
            
            if (questionText) {
                questions.push({ text: questionText, type: questionType });
            }
        }
        
        try {
            const response = await fetch(`/api/surveys/${surveyId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ questions })
            });
            
            if (response.ok) {
                toastManager.success('Survey saved successfully');
                await this.loadSurveys();
            }
        } catch (error) {
            toastManager.error('Failed to save survey');
        }
    }

    async viewResults(surveyId) {
        try {
            const response = await fetch(`/api/surveys/${surveyId}/results`);
            if (response.ok) {
                const results = await response.json();
                this.renderSurveyResults(results);
            }
        } catch (error) {
            toastManager.error('Failed to load survey results');
        }
    }

    renderSurveyResults(results) {
        const resultsContainer = document.getElementById('surveyResults');
        
        if (!results.responses || results.responses.length === 0) {
            resultsContainer.innerHTML = '<p class="text-muted">No responses yet</p>';
            return;
        }
        
        let html = `
            <div class="mb-3">
                <h6>${results.survey_title}</h6>
                <p class="text-muted">${results.responses_count} responses collected</p>
            </div>
        `;
        
        results.questions.forEach((question, index) => {
            html += `
                <div class="card mb-3">
                    <div class="card-body">
                        <h6>${question.text}</h6>
                        <div class="mt-2">
                            ${this.renderQuestionResults(question, results.responses)}
                        </div>
                    </div>
                </div>
            `;
        });
        
        resultsContainer.innerHTML = html;
    }

    renderQuestionResults(question, responses) {
        if (question.type === 'rating') {
            const ratings = responses.map(r => r.answers[question.index]).filter(r => r);
            const avg = ratings.reduce((a, b) => a + b, 0) / ratings.length || 0;
            
            return `
                <div class="progress mb-2">
                    <div class="progress-bar" style="width: ${(avg / 5) * 100}%">Average: ${avg.toFixed(1)}/5</div>
                </div>
                <small class="text-muted">Average rating from ${ratings.length} responses</small>
            `;
        } else if (question.type === 'yesno') {
            const answers = responses.map(r => r.answers[question.index]).filter(r => r);
            const yesCount = answers.filter(a => a === 'Yes').length;
            const noCount = answers.filter(a => a === 'No').length;
            
            return `
                <div class="row">
                    <div class="col-6">
                        <div class="progress">
                            <div class="progress-bar bg-success" style="width: ${(yesCount / answers.length) * 100}%">Yes: ${yesCount}</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="progress">
                            <div class="progress-bar bg-danger" style="width: ${(noCount / answers.length) * 100}%">No: ${noCount}</div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            const answers = responses.map(r => r.answers[question.index]).filter(r => r);
            return `
                <div class="list-group">
                    ${answers.slice(0, 5).map(answer => `<div class="list-group-item">${answer}</div>`).join('')}
                    ${answers.length > 5 ? `<div class="list-group-item text-muted">... and ${answers.length - 5} more</div>` : ''}
                </div>
            `;
        }
    }
}

// Initialize survey system
let surveyManager;

document.addEventListener('DOMContentLoaded', function() {
    surveyManager = new SurveyManager();
});

window.surveyManager = surveyManager;
