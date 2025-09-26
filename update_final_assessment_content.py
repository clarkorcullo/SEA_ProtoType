#!/usr/bin/env python3
"""
Update Final Assessment module content to show only essential information
"""

from app import app, db
from data_models.content_models import Module

def update_final_assessment_content():
    """Update Final Assessment module content to remove technical details"""
    
    with app.app_context():
        # Get the Final Assessment module
        module = Module.query.get(6)
        
        if not module:
            print("❌ Final Assessment module not found!")
            return False
        
        # New simplified content
        new_content = '''
        <div class="module-drawer-container">
            <!-- Level 1: Main Header - Final Assessment -->
            <div class="drawer-header" onclick="toggleDrawer('final-assessment')">
                <div class="drawer-content">
                    <div class="drawer-icon">
                        <i class="fas fa-bullseye"></i>
                    </div>
                    <div class="drawer-title">
                        <h3>Final Assessment</h3>
                        <p>Comprehensive assessment covering all aspects of social engineering awareness and prevention</p>
                    </div>
                    <div class="drawer-arrow">
                        <i class="fas fa-chevron-down" id="arrow-final-assessment"></i>
                    </div>
                </div>
            </div>

            <!-- Module Content (Hidden by default) -->
            <div class="drawer-body" id="content-final-assessment" style="display: none;">

                <!-- Level 2: Final Assessment (Gradient) -->
                <div class="drawer-subheader gradient-sub" onclick="toggleDrawer('final-assessment-content')">
                    <div class="drawer-content">
                        <div class="drawer-icon">
                            <i class="fas fa-clipboard-check"></i>
                        </div>
                        <div class="drawer-title">
                            <h4>Final Assessment</h4>
                        </div>
                        <div class="drawer-arrow">
                            <i class="fas fa-chevron-down" id="arrow-final-assessment-content"></i>
                        </div>
                    </div>
                </div>

                <div class="drawer-subbody" id="content-final-assessment-content" style="display: none;">
                    <div class="content-wrapper">
                        <div class="assessment-rules">
                            <h5><strong>Assessment Rules:</strong></h5>     
                            <ul>
                                <li><strong>25 Items with 80% passing rate</strong></li>
                                <li><strong>3 attempts every 24hrs (in case of failing grade)</strong></li>
                            </ul>

                            <div class="assessment-actions">
                                <a href="/assessment/start" class="btn btn-primary btn-lg" onclick="return confirm('Are you ready to start the Final Assessment? You will have 2 hours to complete 25 questions.')">
                                    <i class="fas fa-play"></i> Start Final Assessment
                                </a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Level 2: Survey (Gradient) -->
                <div class="drawer-subheader gradient-sub" onclick="toggleDrawer('survey')">
                    <div class="drawer-content">
                        <div class="drawer-icon">
                            <i class="fas fa-poll"></i>
                        </div>
                        <div class="drawer-title">
                            <h4>Survey - Google Survey Form</h4>
                        </div>
                        <div class="drawer-arrow">
                            <i class="fas fa-chevron-down" id="arrow-survey"></i>
                        </div>
                    </div>
                </div>

                <div class="drawer-subbody" id="content-survey" style="display: none;">
                    <div class="content-wrapper">
                        <div class="survey-info">
                            <h5><strong>Satisfaction Survey</strong></h5>   
                            <p>Please complete the satisfaction survey to generate your Certificate of Completion.</p>
                            <div class="survey-link">
                                <a href="#" class="btn btn-success btn-lg" target="_blank">
                                    <i class="fas fa-external-link-alt"></i> Take Survey
                                </a>
                                <p class="text-muted mt-2"><small>Survey link will be provided soon</small></p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Level 2: Certificate (Gradient) -->
                <div class="drawer-subheader gradient-sub" onclick="toggleDrawer('certificate')">
                    <div class="drawer-content">
                        <div class="drawer-icon">
                            <i class="fas fa-certificate"></i>
                        </div>
                        <div class="drawer-title">
                            <h4>Certificate</h4>
                        </div>
                        <div class="drawer-arrow">
                            <i class="fas fa-chevron-down" id="arrow-certificate"></i>
                        </div>
                    </div>
                </div>

                <div class="drawer-subbody" id="content-certificate" style="display: none;">
                    <div class="content-wrapper">
                        <div class="certificate-info">
                            <h5><strong>Certificate of Completion</strong></h5>
                            <p>Generate your certificate after completing the Final Assessment and Survey.</p>
                            <div class="certificate-requirements">
                                <div class="requirement-item">
                                    <i class="fas fa-check-circle text-success"></i>
                                    <span>Pass Final Assessment (80% or higher)</span>
                                </div>
                                <div class="requirement-item">
                                    <i class="fas fa-check-circle text-success"></i>
                                    <span>Complete Satisfaction Survey</span>
                                </div>
                            </div>
                            <div class="certificate-actions">
                                <button class="btn btn-warning btn-lg" onclick="generateCertificate()" disabled>
                                    <i class="fas fa-download"></i> Generate Certificate
                                </button>
                                <p class="text-muted mt-2"><small>Complete all requirements to unlock certificate generation</small></p>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <style>
        /* Drawer Container Styles */
        .module-drawer-container {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;   
            max-width: 100%;
            margin: 0 auto;
        }

        /* Level 1: Main Header - Gradient Background */
        .drawer-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  
            color: white;
            border-radius: 12px;
            margin-bottom: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .drawer-header:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }

        /* Level 2: Sub Header - Gradient Background */
        .drawer-subheader {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);  
            color: white;
            border-radius: 10px;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .drawer-subheader:hover {
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        }

        /* Drawer Content Layout */
        .drawer-content {
            display: flex;
            align-items: center;
            padding: 15px 20px;
            gap: 15px;
        }

        .drawer-icon {
            font-size: 1.5rem;
            min-width: 30px;
            text-align: center;
        }

        .drawer-title h3, .drawer-title h4, .drawer-title h5 {
            margin: 0;
            font-weight: 600;
        }

        .drawer-title p {
            margin: 5px 0 0 0;
            opacity: 0.9;
            font-size: 0.9rem;
        }

        .drawer-arrow {
            margin-left: auto;
            transition: transform 0.3s ease;
        }

        .drawer-arrow.rotated {
            transform: rotate(180deg);
        }

        /* Content Areas */
        .drawer-body, .drawer-subbody {
            padding: 0 20px 20px 20px;
            animation: slideDown 0.3s ease;
        }

        .content-wrapper {
            line-height: 1.6;
        }

        /* Assessment Specific Styles */
        .assessment-rules {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #007bff;
        }

        .assessment-rules ul {
            margin: 15px 0;
        }

        .assessment-rules li {
            margin: 10px 0;
        }

        .assessment-actions {
            text-align: center;
            margin-top: 20px;
        }

        .survey-info, .certificate-info {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
        }

        .survey-link, .certificate-actions {
            text-align: center;
            margin-top: 20px;
        }

        .certificate-requirements {
            margin: 20px 0;
        }

        .requirement-item {
            display: flex;
            align-items: center;
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border: 1px solid #dee2e6;
        }

        .requirement-item i {
            margin-right: 10px;
            font-size: 1.2rem;
        }

        /* Animations */
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .drawer-content {
                padding: 12px 15px;
                gap: 10px;
            }

            .drawer-icon {
                font-size: 1.2rem;
            }

            .drawer-title h3 {
                font-size: 1.1rem;
            }

            .drawer-title h4 {
                font-size: 1rem;
            }

            .drawer-title h5 {
                font-size: 0.9rem;
            }
        }
        </style>

        <script>
        function toggleDrawer(id) {
            const content = document.getElementById('content-' + id);       
            const arrow = document.getElementById('arrow-' + id);

            if (content.style.display === 'none' || content.style.display === '') {
                content.style.display = 'block';
                arrow.classList.add('rotated');
            } else {
                content.style.display = 'none';
                arrow.classList.remove('rotated');
            }
        }

        function generateCertificate() {
            // Generate certificate logic
            alert('Certificate generation will be implemented soon!');      
        }
        </script>
        '''
        
        # Update the module content
        module.content = new_content
        db.session.commit()
        
        print("✅ Final Assessment module content updated successfully!")
        print("✅ Removed technical details from Assessment Rules")
        print("✅ Now shows only essential information: 25 items, 80% passing, 3 attempts every 24hrs")
        
        return True

if __name__ == "__main__":
    update_final_assessment_content()

