pipeline {
    agent any

    environment {
        IMAGE_TAG = "latest"
        CONTAINER_NAME = "my_flask_container"
    }

    triggers {
    cron('H 0 * * *')  // Runs once a day at midnight
}

    stages {
        stage('Checkout') {
            steps {
                // Pull the code from the GitHub repository, specify 'main' branch
                git branch: 'main', url: 'https://github.com/yaashwin/jenkins_flask_project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image using the Dockerfile in the repo
                    sh 'docker build -t flask_image_lts .'
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    // Stop and remove the existing container if it's running
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
                    // Run the new container with the built image
                    sh "docker run -d --name flask_container -p 8081:5000 flask_image_lts"
                }
            }
        }
    }

    post {
        always {
            // Clean up unused Docker images and containers
            sh 'docker system prune -f'
        }
    }
}
