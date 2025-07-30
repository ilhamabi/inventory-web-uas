pipeline {
    agent any

    environment {
        SONARQUBE_SCANNER = 'SonarScanner' // Sesuaikan dengan konfigurasi Sonar di Jenkins
        DOCKER_IMAGE = 'inventory-web:latest' // Ganti sesuai nama image yang kamu inginkan
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Code sudah otomatis ditarik dari GitHub oleh Jenkins.'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
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

        stage('Build & Deploy with Docker') {
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

