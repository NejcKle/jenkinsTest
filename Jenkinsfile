pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Running setup...'
                sh 'pip3 install -r unit_test_requirements.txt'
                sh 'python3 tca9548a.py'
            }
        }
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                sh 'python3 -m unittest -v test_pcf8591.py'
            }
        }
        stage('Hardware Testing') {
            steps {
                echo 'Running hardware tests...'
            }
        }
    
    }
}