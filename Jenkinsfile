pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'  
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    cleanWs()
                    bat 'git clone https://github.com/Bettaieb-Roua/projet-docker.git .'
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    // Construire les images Docker
                    bat 'docker-compose build'
                }
            }
        }
        stage('Start Docker Services') {
            steps {
                script {
                    // Démarrer les services Docker
                    bat 'docker-compose up -d'
                }
            }
        }
        stage('Run Unit Tests') {
            steps {
                script {
                    // Lancer les tests avec unittest
                    bat 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m unittest discover App/tests/ > result.log'
                    bat 'C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python312\\python.exe -m unittest discover VggApp/tests/ > result.log'
                }
            }
        }
    }

    post {
        always {
            // Arrêter et nettoyer les services Docker après exécution
            script {
                bat 'docker-compose down'
            }
        }
    }
}
