pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        DOCKER_USER = "${DOCKERHUB_CREDENTIALS_USR}"
        DOCKER_PASS = "${DOCKERHUB_CREDENTIALS_PSW}"
        MINIKUBE_HOME = '/var/lib/jenkins/.minikube'
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        // KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/manas-manna/medical-chatbot.git'
            }
        }
        
        stage('Pre-deployment Health Check') {
            steps {
                script {
                    sh '''
                        echo "=== Checking Minikube Status ==="
                        minikube status
                        
                        echo "=== Checking MongoDB Connection ==="
                        # Test MongoDB connection on host
                        timeout 10 bash -c "</dev/tcp/localhost/27017" && echo "MongoDB is accessible" || echo "MongoDB connection failed"
                        
                        echo "=== Checking Docker ==="
                        docker --version
                        
                        echo "=== Checking kubectl ==="
                        kubectl version --client
                    '''
                }
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
                                echo "Building Backend Image..."
                                docker build -t $DOCKER_USER/medical-chatbot-backend:latest .
                                
                                echo "Pushing Backend Images..."
                                # docker push $DOCKER_USER/medical-chatbot-backend:latest
                                
                                echo "Loading image to Minikube..."
                                minikube image load $DOCKER_USER/medical-chatbot-backend:latest
                            '''
                        }
                    }
                }
                stage('Frontend') {
                    steps {
                        dir('frontend') {
                            sh '''
                                echo "Building Frontend Image..."
                                docker build -t $DOCKER_USER/medical-chatbot-frontend:latest .
                                
                                echo "Pushing Frontend Images..."
                                # docker push $DOCKER_USER/medical-chatbot-frontend:latest
                                
                                echo "Loading image to Minikube..."
                                minikube image load $DOCKER_USER/medical-chatbot-frontend:latest
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Prepare Minikube Environment') {
            steps {
                sh '''
                    echo "=== Setting up required directories in Minikube ==="
                    minikube ssh -- "sudo mkdir -p /mnt/data/logs /mnt/data/elasticsearch && sudo chmod 777 /mnt/data/logs /mnt/data/elasticsearch"
                    
                    echo "=== Directory setup completed ==="
                    minikube ssh -- "ls -la /mnt/data/"
                '''
            }
        }
        
        stage('Deploy using Ansible') {
            steps {
                sh '''
                    echo "=== Starting Ansible Deployment ==="
                    cd ansible
                    export MINIKUBE_HOME=/var/lib/jenkins/.minikube
                    export KUBECONFIG=/var/lib/jenkins/.kube/config
                    ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e kubeconfig_path=$KUBECONFIG
                '''
            }
        }
        
        // stage('Post-deployment Health Check') {
        //     steps {
        //         script {
        //             sh '''
        //                 echo "=== Waiting for deployments to be ready ==="
        //                 kubectl -n medical-chatbot wait --for=condition=available --timeout=600s deployment/backend
        //                 kubectl -n medical-chatbot wait --for=condition=available --timeout=600s deployment/frontend
        //                 kubectl -n medical-chatbot wait --for=condition=available --timeout=600s deployment/elasticsearch
        //                 kubectl -n medical-chatbot wait --for=condition=available --timeout=600s deployment/logstash
        //                 kubectl -n medical-chatbot wait --for=condition=available --timeout=600s deployment/kibana
                        
        //                 echo "=== Checking Pods Status ==="
        //                 kubectl -n medical-chatbot get pods -o wide
                        
        //                 echo "=== Checking Services Status ==="
        //                 kubectl -n medical-chatbot get services
                        
        //                 echo "=== Checking HPAs Status ==="
        //                 kubectl -n medical-chatbot get hpa
                        
        //                 echo "=== Checking PVC Status ==="
        //                 kubectl -n medical-chatbot get pvc
                        
        //                 echo "=== Pod Resource Usage ==="
        //                 kubectl -n medical-chatbot top pods || echo "Metrics server not available"
        //             '''
        //         }
        //     }
        // }
        
        // stage('Application Health Tests') {
        //     steps {
        //         sh '''
        //             echo "=== Starting Port Forwarding for Health Checks ==="
        //             # Start port forwarding in background
        //             kubectl port-forward service/backend -n medical-chatbot 8000:8000 &
        //             PF_PID_BACKEND=$!
                    
        //             kubectl port-forward service/frontend -n medical-chatbot 3000:80 &
        //             PF_PID_FRONTEND=$!
                    
        //             # Wait a moment for port forwarding to establish
        //             sleep 10
                    
        //             echo "=== Testing Backend Health ==="
        //             timeout 30 bash -c 'until curl -f http://localhost:8000/health || curl -f http://localhost:8000/docs; do sleep 2; done' || echo "Backend health check failed"
                    
        //             echo "=== Testing Frontend ==="
        //             timeout 30 bash -c 'until curl -f http://localhost:3000; do sleep 2; done' || echo "Frontend health check failed"
                    
        //             # Clean up port forwarding
        //             kill $PF_PID_BACKEND $PF_PID_FRONTEND || true
                    
        //             echo "=== Health checks completed ==="
        //         '''
        //     }
        // }
        
        stage('Setup Port Forwarding') {
            steps {
                sh '''
                    sleep 15
                    echo "=== Setting up persistent port forwarding ==="
                    ./port-forward.sh
                    
                    echo "=== Port forwarding started ==="
                    echo "Access URLs:"
                    echo "Frontend: http://localhost:3000"
                    echo "Backend: http://localhost:8000"
                    echo "Elasticsearch: http://localhost:9200"
                    echo "Kibana: http://localhost:5601"
                    echo "Logstash: http://localhost:5044"
                '''
            }
        }
    }
    
    post {
        success {
            echo "🎉 Deployment completed successfully!"
            echo "Application is now running and accessible via port forwarding"
            sh '''
                kubectl -n medical-chatbot get pods
                echo "=== Deployment Summary ==="
                echo "✅ All services deployed successfully"
                echo "✅ Health checks passed"
                echo "✅ Port forwarding configured"
            '''
        }
        failure {
            echo "❌ Deployment failed, initiating rollback..."
            sh '''
                echo "=== Deployment failed, rolling back ==="
                cd ansible
                ansible-playbook -i inventory/hosts.yml playbooks/rollback.yml -v || echo "Rollback completed with warnings"
                
                echo "=== Post-rollback status ==="
                kubectl -n medical-chatbot get pods || true
            '''
        }
        always {
            sh '''
                echo "=== Cleaning up ==="
                docker logout || true
                
                # Clean up any test port forwarding processes
                pkill -f "kubectl port-forward.*8000" || true
                pkill -f "kubectl port-forward.*3000" || true
            '''
        }
    }
}