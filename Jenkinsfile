pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
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
                "sh 'python3 ./test_pcf_system.py'"
            }
        }
    
    }
}