pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Bettaieb-Roua/projet-docker.git'
            }
        }
        stage('Check Docker Version') {
            steps {
                script {
                    bat 'docker --version'
                }
            }
        }
        stage('Build Docker Images') {
            steps {
                script {
                    bat 'docker-compose build'
                }
            }
        }
        stage('Run Containers') {
            steps {
                script {
                    bat 'docker-compose up -d'
                }
            }
        }
        
    }
}