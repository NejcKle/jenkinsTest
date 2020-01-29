pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'pip3 install -r test_requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 ./test_pcf8591.py'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    
    }
}