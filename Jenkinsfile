pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Running setup...'
                sh 'pip3 install -r unit_test_requirements.txt'
            }
        }
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                sh 'python3 ./test_pcf8591.py'
            }
        }
        stage('Hardware Testing') {
            steps {
                echo 'Running hardware tests...'
            }
        }
    
    }
}