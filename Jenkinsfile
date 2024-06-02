pipeline {
    agent { 
      label "jenkins-agent" 
    }
    
    stages {
      stage("Container Building") {
        steps {
          script {
            dir("${env.PWD}") {
              sh "docker compose up --build -d"
            }
          }
        }
      }

      stage("Code analysis") {
        steps {
          script {
            dir("${env.PWD}") {
              withSonarQubeEnv('mlops_platform') {
                withCredentials([string(credentialsId: 'jenkins-sonarqube', variable: 'SONAR_TOKEN')]) {
                  sh '''
                    sleep 20
                    docker exec -u root sonarqube sh -c "sonar-scanner \
                      -Dsonar.projectKey=mlops_platform \
                      -Dsonar.sources=. \
                      -Dsonar.login=$SONAR_TOKEN"
                  '''
                }
              }
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
    }
}
