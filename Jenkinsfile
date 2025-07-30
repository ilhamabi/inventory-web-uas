pipeline {
    agent any

    tools {
        python 'Python3'  // Harus sudah dikonfigurasi di Jenkins Global Tools
    }

    environment {
        SONARQUBE_SCANNER = 'SonarScanner'     // Name from Jenkins Global Tool Config
        DOCKER_IMAGE = 'inventory-web:latest'  // Nama image yang akan dibuat
    }

    stages {
        stage('Checkout Source Code') {
            steps {
                // Otomatis clone repo GitHub (jika pipeline dari SCM Git)
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Unit Tests with Coverage') {
            steps {
                sh 'pytest --cov=app --cov-report=xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('LocalSonar') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Build and Deploy Docker') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                    sh 'docker stop inventory-web || true'
                    sh 'docker rm inventory-web || true'
                    sh 'docker run -d --name inventory-web -p 5000:5000 $DOCKER_IMAGE'
                }
            }
        }
    }
}


