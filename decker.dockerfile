pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = credentials('i210298@nu.edu.pk')  // Use the ID you assigned in Jenkins credentials
        DOCKER_IMAGE = "ibrahimabid0/your-app-name"         // Docker Hub image name
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/IbrahimAbid0/MLOps-Class-Activity-03.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image
                script {
                    docker.build("${DOCKER_IMAGE}")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'DOCKERHUB_CREDENTIALS') {
                        docker.image("${DOCKER_IMAGE}").push("latest")
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Docker Image pushed to Docker Hub successfully.'
        }
        failure {
            echo 'Failed to push Docker Image.'
        }
    }
}
