version: "1.0"

trigger:
  cron: "*/2 * * * *"  # Every 2 minutes

stages:
  - name: Checkout
    steps:
      - checkout:
          url: "https://github.com/yaashwin/jenkins_flask_project.git"

  - name: Build Docker Image
    steps:
      - script:
          name: Build Docker Image
          command: |
            docker build -t flask_image_lts .

  - name: Stop Existing Container
    steps:
      - script:
          name: Stop Existing Docker Container
          command: |
            if [ $(docker ps -q -f name=flask_container) ]; then
                docker stop flask_container
                docker rm flask_container
            fi

  - name: Run New Container
    steps:
      - script:
          name: Run New Docker Container
          command: |
            docker run -d --name flask_container -p 8080:5000 flask_image_lts

post:
  always:
    steps:
      - script:
          name: Clean Up Docker System
          command: |
            docker system prune -f

