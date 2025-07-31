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
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests with Coverage') {
            steps {
               sh '''
                    . venv/bin/activate
                    PYTHONPATH=. pytest --cov=app --cov-report=xml
               '''
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
                    sh 'docker run -d --name inventory-web -p 5000:5000 -v $WORKSPACE/logs:/var/log/app $DOCKER_IMAGE'
                }
            }
        }
    }
}

