pipeline {
    agent any

    environment {
        // Define environment variables if needed
        PYTHONPATH = "${WORKSPACE}"
    }

    stages {
        stage('Clone Code') {
            steps {
                // Clone the repository
                git branch: 'main', url: 'https://github.com/itsdivyanshjha/DevSecOps-CICD.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    // Install Python dependencies
                    sh '''
                        python3 -m pip install --user --upgrade pip
                        python3 -m pip install --user -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests and Generate Coverage') {
            steps {
                script {
                    // Run tests with coverage
                    sh '''
                        python3 -m pytest test_app.py --cov=app --cov-report=xml:coverage.xml --cov-report=term
                    '''
                }
                
                // Archive test results if you want
                publishTestResults testResultsPattern: 'coverage.xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // Run SonarQube analysis
                withSonarQubeEnv('Sonar') {
                    sh '''
                        ${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=simple-flask-app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN}
                    '''
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
                script {
                    // Install and run Bandit for security scanning
                    sh '''
                        python3 -m pip install --user bandit
                        python3 -m bandit -r . -f json -o bandit-report.json || true
                        python3 -m bandit -r . || true
                    '''
                }
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