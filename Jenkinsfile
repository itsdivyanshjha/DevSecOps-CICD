pipeline {
    agent any
    environment {
        // Defines the SonarQube Scanner tool for easy access
        SONAR_HOME = tool "Sonar"
    }
    stages {
        stage("Clone repo from GitHub") {
            steps {
                git url: "https://github.com/itsdivyanshjha/DevSecOps-CICD.git", branch: "main"
            }
        }

        stage("SonarQube Quality Analysis") {
            steps {
                withSonarQubeEnv("Sonar") {
                    sh "$SONAR_HOME/bin/sonar-scanner -Dsonar.projectName=DevSecOps-CICD -Dsonar.projectKey=DevSecOps-CICD"
                }
            }
        }

        stage("OWASP Dependency Check") {
            steps {
                dependencyCheck additionalArguments: '--scan ./', odcInstallation: 'OWASP-DC'
                dependencyCheckPublisher(
                    pattern: 'dependency-check-report.xml',
                    failedTotalHigh: '0',
                    unstableTotalHigh: '0'
                )
            }
        }

        stage("Sonar Quality Gate Scan") {
            steps {
                timeout(time: 2, unit: "MINUTES") {
                    waitForQualityGate abortPipeline: false
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building the Docker image...'
                sh 'docker-compose build'
            }
        }
        
        stage("Trivy Image Scan") {
            steps {
                sh 'wget https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl -O trivy-template.tpl'
                sh 'trivy image --format template --template "@trivy-template.tpl" -o trivy-image-report.html devsecops-pipeline_webapp:latest'
            }
            post {
                always {
                    publishHTML(
                        target: [
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'trivy-image-report.html',
                            reportName: 'Trivy Image Report'
                        ]
                    )
                }
            }
        }

        // --- UPDATED DEPLOYMENT STAGE ---
        stage('Deploy Application') {
            steps {
                echo 'Stopping and removing any old containers to prevent conflicts...'
                // This command cleans up the previous deployment first
                sh 'docker-compose down'

                echo 'Deploying the new, scanned application...'
                // This command starts the new version
                sh 'docker-compose up -d'
            }
        }

        stage('Dynamic Security Scan (DAST) with ZAP') {
            steps {
                echo 'Starting DAST scan against the running application...'
                sh '''
                    docker run --network devsecops-network --rm \
                    -v $(pwd):/zap/wrk/:rw \
                    owasp/zap2docker-stable zap-full-scan.py \
                    -t http://devsecops_app:5000 \
                    -r zap_report.html
                '''
            }
            post {
                always {
                    publishHTML(
                        target: [
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: '.',
                            reportFiles: 'zap_report.html',
                            reportName: 'ZAP DAST Report'
                        ]
                    )
                }
            }
        }
    }
    post {
        // This 'always' block runs at the very end to clean everything up
        always {
            echo 'Cleaning up all containers and networks...'
            sh 'docker-compose down'
        }
    }
}