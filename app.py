from flask import Flask, render_template_string
import datetime

# Create an instance of the Flask class
app = Flask(__name__)

# HTML template for the DevSecOps pipeline showcase
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevSecOps Pipeline Showcase</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .pipeline-container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
        
        .pipeline-title {
            text-align: center;
            font-size: 2rem;
            color: #2c3e50;
            margin-bottom: 30px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        
        .step {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #3498db;
            transition: transform 0.3s ease;
        }
        
        .step:hover {
            transform: translateX(10px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .step-number {
            background: #3498db;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 20px;
            flex-shrink: 0;
        }
        
        .step-content {
            flex: 1;
        }
        
        .step-title {
            font-size: 1.3rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .step-description {
            color: #666;
            line-height: 1.6;
        }
        
        .step-tools {
            background: #e8f4fd;
            padding: 8px 12px;
            border-radius: 5px;
            margin-top: 8px;
            font-size: 0.9rem;
            color: #2980b9;
        }
        
        .status-badge {
            background: #27ae60;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-left: 15px;
        }
        
        .experiment-info {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .experiment-title {
            font-size: 1.8rem;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .experiment-description {
            color: #666;
            line-height: 1.8;
            font-size: 1.1rem;
            text-align: justify;
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 30px;
            opacity: 0.8;
        }
        
        .tech-stack {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        
        .tech-stack h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .tech-tag {
            background: #3498db;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 DevSecOps Pipeline Showcase</h1>
            <p>Complete CI/CD Pipeline with Security Scanning & Quality Gates</p>
        </div>
        
        <div class="pipeline-container">
            <h2 class="pipeline-title">🔄 Pipeline Stages</h2>
            
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <div class="step-title">Code Push to GitHub</div>
                    <div class="step-description">
                        Developer pushes code changes to the main branch, triggering the automated pipeline.
                        This demonstrates modern GitOps practices with version control integration.
                    </div>
                    <div class="step-tools">Tools: Git, GitHub, Jenkins Webhook</div>
                </div>
                <div class="status-badge">✅ Complete</div>
            </div>
            
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <div class="step-title">SonarQube SAST Analysis</div>
                    <div class="step-description">
                        Static Application Security Testing (SAST) scans the codebase for security vulnerabilities,
                        code smells, and quality issues. Generates detailed reports and enforces quality gates.
                    </div>
                    <div class="step-tools">Tools: SonarQube Scanner, Quality Gates</div>
                </div>
                <div class="status-badge">✅ Complete</div>
            </div>
            
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <div class="step-title">OWASP Dependency Check</div>
                    <div class="step-description">
                        Scans all project dependencies (Python packages) for known vulnerabilities using
                        the OWASP dependency-check tool. Identifies outdated or vulnerable libraries.
                    </div>
                    <div class="step-tools">Tools: OWASP Dependency Check, NVD Database</div>
                </div>
                <div class="status-badge">✅ Complete</div>
            </div>
            
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <div class="step-title">Trivy Container Scan</div>
                    <div class="step-description">
                        Scans the Docker image for vulnerabilities in the base image and application layers.
                        Provides comprehensive security analysis of the containerized application.
                    </div>
                    <div class="step-tools">Tools: Trivy Scanner, Docker Registry</div>
                </div>
                <div class="status-badge">✅ Complete</div>
            </div>
            
            <div class="step">
                <div class="step-number">5</div>
                <div class="step-content">
                    <div class="step-title">Docker Unit Tests</div>
                    <div class="step-description">
                        Runs comprehensive unit tests within the Docker container environment to ensure
                        application functionality and generate test coverage reports.
                    </div>
                    <div class="step-tools">Tools: pytest, coverage.py, Docker</div>
                </div>
                <div class="status-badge">✅ Complete</div>
            </div>
            
            <div class="step">
                <div class="step-number">6</div>
                <div class="step-content">
                    <div class="step-title">Jenkins Container Deployment</div>
                    <div class="step-description">
                        Automated deployment to production using Jenkins container orchestration.
                        Implements blue-green deployment strategy with rollback capabilities.
                    </div>
                    <div class="step-tools">Tools: Jenkins, Docker Compose, Container Orchestration</div>
                </div>
                <div class="status-badge">✅ Complete</div>
            </div>
        </div>
        
        <div class="experiment-info">
            <h2 class="experiment-title">🧪 Experiment Overview</h2>
            <div class="experiment-description">
                <p><strong>Objective:</strong> This experiment demonstrates a complete DevSecOps pipeline that integrates security scanning, quality assurance, and automated deployment into a single, streamlined process.</p>
                
                <p><strong>Key Achievements:</strong></p>
                <ul style="margin-left: 20px; margin-top: 10px;">
                    <li>Successfully implemented SAST scanning with SonarQube quality gates</li>
                    <li>Integrated OWASP dependency vulnerability scanning</li>
                    <li>Added container security scanning with Trivy</li>
                    <li>Implemented automated unit testing with coverage reporting</li>
                    <li>Created containerized deployment pipeline</li>
                    <li>Established security-first CI/CD practices</li>
                </ul>
                
                <p><strong>Security Focus:</strong> This pipeline ensures that security is not an afterthought but integrated into every stage of the development process, from code commit to deployment.</p>
                
                <div class="tech-stack">
                    <h3>🛠️ Technology Stack</h3>
                    <div class="tech-tags">
                        <span class="tech-tag">Jenkins</span>
                        <span class="tech-tag">SonarQube</span>
                        <span class="tech-tag">OWASP</span>
                        <span class="tech-tag">Trivy</span>
                        <span class="tech-tag">Docker</span>
                        <span class="tech-tag">Python</span>
                        <span class="tech-tag">Flask</span>
                        <span class="tech-tag">pytest</span>
                        <span class="tech-tag">GitHub</span>
                        <span class="tech-tag">DevSecOps</span>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Pipeline Status: <strong>SUCCESS</strong> | Last Updated: {{ current_time }}</p>
            <p>DevSecOps Pipeline Experiment - Demonstrating Security-First CI/CD Practices</p>
        </div>
    </div>
</body>
</html>
'''

# Define a route for the root URL '/'
@app.route('/')
def home():
    """This function runs when someone visits the main page."""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HTML_TEMPLATE, current_time=current_time)

# Run the app
if __name__ == '__main__':
    # Bind to 0.0.0.0 to make it accessible from outside the container
    app.run(host='0.0.0.0', port=5000)