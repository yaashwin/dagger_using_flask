pipeline {
    agent any
    
    environment {
        IMAGE_TAG = "latest"
        CONTAINER_NAME = "my_flask_container"
    }
    
    triggers {
        // Schedule the pipeline to run every 2 minutes
        cron('*/2 * * * *') // Every 2 minutes
    }
    
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/yaashwin/jenkins_flask_project.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t flask_image_lts .'
                }
            }
        }
        
        stage('Stop Existing Container') {
            steps {
                script {
                    sh """
                        if [ \$(docker ps -q -f name=flask_container) ]; then
                            docker stop flask_container
                            docker rm flask_container
                        fi
                    """
                }
            }
        }
        
        stage('Run New Container') {
            steps {
                script {
                    sh "docker run -d --name flask_container -p 8080:5000 flask_image_lts"
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker system prune -f'
        }
    }
}
