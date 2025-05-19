pipeline {
  agent any
  environment {
    DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
    DOCKER_USER = "${DOCKERHUB_CREDENTIALS_USR}"
    DOCKER_PASS = "${DOCKERHUB_CREDENTIALS_PSW}"
    KUBECONFIG = credentials('kubeconfig')
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
    stage('Deploy using Ansible') {
      steps {
        sh '''
          cd ansible
          ansible-playbook -i inventory/hosts.yml playbooks/deploy_app.yml
        '''
      }
    }
    stage('Verify Deployment') {
      steps {
        sh '''
          export KUBECONFIG=${KUBECONFIG}
          echo "Checking Pods Status:"
          kubectl -n expense-tracker get pods
          
          echo "Checking Services Status:"
          kubectl -n expense-tracker get services
          
          echo "Checking HPAs Status:"
          kubectl -n expense-tracker get hpa
        '''
      }
    }
  }
  post {
    success {
      echo "Deployment completed successfully!"
    }
    failure {
      sh '''
        export KUBECONFIG=${KUBECONFIG}
        echo "Deployment failed, rolling back..."
        # Let Ansible handle rollback
        cd ansible
        ansible-playbook -i inventory/hosts.yml playbooks/rollback.yml
      '''
    }
    always {
      sh '''
        docker logout
      '''
    }
  }
}
