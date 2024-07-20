pipeline {
  agent { 
    label "jenkins-agent" 
  }
  
  environment {
      BASE_DIR = "${env.CURRENT_WD}"
  }
  
  stages {
    stage("Container Building") {
      steps {
        script {
          dir("${env.PWD}") {
            sh "docker compose up --build -d"
            
            sh "minikube start"
          }
        }
      }
    }

    stage("Data Pipeline") {
      steps {
        sh 'docker exec pipeline sh -c "dagster asset materialize -m pipeline --select \\"*\\""'
      }
    }

    stage("Feast Materialization") {
      steps {
        sh 'docker exec mtl_pipeline sh -c "dagster job execute -m mtl_pipeline"'
      }
    }

    stage("Training Pipeline") {
      steps {
        sh 'docker exec training_pipeline sh -c "dagster asset materialize -m training_pipeline --select \\"*\\""'
      }
    }

    stage('Docker Image Building and Pushing ') {
      steps {
        script {
          dir("${BASE_DIR}/src/data/model_serving/deloyment") {
            sh 'docker build -t kyphan3802/api_model:latest .'
          
              sh 'docker push kyphan3802/api_model:latest'
            }
          }
        }
    }

    stage('Model Deployment') {
      steps {
        script {
          dir("${BASE_DIR}/minikube") {
            sh 'kubectl delete pods --all'

            sh 'kubectl apply -f deployment.yaml && kubectl apply -f service.yaml'
          }
        }
      }
    }
    stage('Prometheus and Grafana Deployment') {
      steps {
        script {
          dir("${BASE_DIR}/minikube") {
            sh 'kubectl apply -f prometheus-deployment.yaml && kubectl apply -f prometheus-service.yaml'
            
            sh 'kubectl apply -f grafana-datasource.yaml && kubectl apply -f grafana-deployment.yaml && kubectl apply -f grafana-service.yaml'
            
          }
        }
      }
    }
  }
}

