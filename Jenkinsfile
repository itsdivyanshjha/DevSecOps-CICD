pipeline {
    agent any

    environment {
        // Define environment variables if needed
        PYTHONPATH = "${WORKSPACE}"
        SONAR_HOME=tool"Sonar"
    }

    stages {
        stage('Clone Code') {
            steps {
                // Clone the repository
                git branch: 'main', url: 'https://github.com/itsdivyanshjha/DevSecOps-CICD.git'
            }
        }

        stage('Setup Python Environment & Run Tests') {
            steps {
                sh '''
                    # Install pip if not available
                    if ! python3 -m pip --version; then
                        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
                        python3 get-pip.py --user
                        rm get-pip.py
                    fi
                    
                    # Install dependencies
                    python3 -m pip install --user --upgrade pip
                    python3 -m pip install --user -r requirements.txt
                    
                    # Run tests with coverage
                    python3 -m pytest test_app.py --cov=app --cov-report=xml:coverage.xml --cov-report=term || true
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // Run SonarQube analysis
                withSonarQubeEnv('Sonar') {
                    sh "${tool('Sonar')}/bin/sonar-scanner"
                }
            }
        }

        stage('Quality Gate Check') {
            steps {
                // Wait for SonarQube analysis and check Quality Gate
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Security Scan with Bandit') {
            steps {
                sh '''
                    # Install and run Bandit for security scanning
                    python3 -m pip install --user bandit
                    python3 -m bandit -r . -f json -o bandit-report.json || true
                    echo "Bandit security scan completed"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    sh 'docker build -t simple-flask-app:${BUILD_NUMBER} .'
                    sh 'docker tag simple-flask-app:${BUILD_NUMBER} simple-flask-app:latest'
                }
            }
        }
    }

    post {
        always {
            // Clean up
            sh 'docker system prune -f'
        }
        
        success {
            echo 'Pipeline completed successfully!'
        }
        
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
    }
}