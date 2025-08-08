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
                    // Runs the SonarQube scanner
                    sh "$SONAR_HOME/bin/sonar-scanner -Dsonar.projectName=DevSecOps-CICD -Dsonar.projectKey=DevSecOps-CICD"
                }
            }
        }

        stage("OWASP Dependency Check") {
            steps {
                // Scans for vulnerabilities in third-party libraries
                dependencyCheck additionalArguments: '--scan ./', odcInstallation: 'OWASP-DC'
                
                // Publishes the OWASP report to the Jenkins dashboard
                dependencyCheckPublisher(
                    pattern: 'dependency-check-report.xml',
                    failedTotalHigh: '0',
                    unstableTotalHigh: '0'
                )
            }
        }

        stage("Sonar Quality Gate Scan") {
            steps {
                // Pauses the pipeline to wait for SonarQube's analysis and quality gate result
                timeout(time: 2, unit: "MINUTES") {
                    waitForQualityGate abortPipeline: false
                }
            }
        }

        // --- NEW STAGE TO BUILD THE IMAGE BEFORE SCANNING ---
        stage('Build Docker Image') {
            steps {
                echo 'Building the Docker image...'
                sh 'docker-compose build'
            }
        }

        // --- UPDATED TRIVY STAGE TO SCAN THE IMAGE ---
        stage("Trivy Image Scan") {
            steps {
                echo 'Scanning the Docker image for vulnerabilities...'
                // Downloads the HTML report template for Trivy
                sh 'wget https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl -O trivy-template.tpl'
                
                // Runs the scan against the image built by docker-compose
                sh 'trivy image --format template --template "@trivy-template.tpl" -o trivy-image-report.html devsecops-pipeline_webapp:latest'
            }
            post {
                always {
                    // Publishes the generated HTML report to the Jenkins build page
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
                echo 'Stopping any old containers to free up the port...'
                // Cleans up the previous deployment first to prevent port conflicts
                sh 'docker-compose down'

                echo 'Deploying the new, scanned application...'
                // Starts the new version without building, as it's already done
                sh 'docker-compose up -d'
            }
        }
    }
}