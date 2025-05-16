pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    DOCKER_USER = "${DOCKERHUB_CREDENTIALS_USR}"
    DOCKER_PASS = "${DOCKERHUB_CREDENTIALS_PSW}"
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/manas-manna/Expense_Tracker.git'
      }
    }

    stage('Docker Login') {
      steps {
        sh '''
          echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
        '''
      }
    }

    stage('Build & Push Images') {
      parallel {
        stage('Backend') {
          steps {
            dir('backend') {
              sh '''
                docker build -t $DOCKER_USER/backend:latest .
                docker push $DOCKER_USER/backend:latest
              '''
            }
          }
        }

        stage('Frontend') {
          steps {
            dir('frontend') {
              sh '''
                docker build -t $DOCKER_USER/frontend:latest .
                docker push $DOCKER_USER/frontend:latest
              '''
            }
          }
        }

        stage('Fraud Detection') {
          steps {
            dir('fraud-detection') {
              sh '''
                docker build -t $DOCKER_USER/fraud-detection:latest .
                docker push $DOCKER_USER/fraud-detection:latest
              '''
            }
          }
        }
      }
    }
  }
}
