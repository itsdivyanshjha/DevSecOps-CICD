pipeline {
    agent any
    environment {
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
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }

        stage("Sonar Quality Gate Scan") {
            steps {
                timeout(time: 2, unit: "MINUTES") {
                    waitForQualityGate abortPipeline: false
                }
            }
        }

        stage("Trivy File System Check") {
            steps {
                sh "trivy fs --format table -o trivy-fs-report.html ."
            }
        }

        // --- NEW DEPLOYMENT STAGE ---
        stage('Deploy Application') {
            steps {
                echo 'Building and deploying the application...'
                sh 'docker-compose up -d --build'
            }
        }
    }
}