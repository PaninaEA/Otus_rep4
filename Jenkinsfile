pipeline {
    agent {
      docker { 
        image 'python:3.11'
      }
    }
stages {
      stage('Run Tests') {
            steps {
                script {
                    sh 'python3 -m pip config set global.trusted-host "pypi.org files.pythonhosted.org"'
                    sh 'python3 -m pip install -r requirements.txt'
                    sh 'pytest'
                }
            }
        }
}
      

    
}
