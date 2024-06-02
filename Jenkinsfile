pipeline {
    agent { 
        label "jenkins-agent" 
    }
    
    // environment {
    //     WORKING_DIR = "${env.PWD}"
    // }

    stages {
        stage("Container Building") {
            steps {
                script{
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
                withSonarQubeEnv(installationName: "mlops_platform") {
                    sh "sonar-scanner \
                        -Dsonar.projectKey=mlops_platform \
                        -Dsonar.sources=."
                }
              }
            }
          }
        }
        // stage("Data Pipeline") {
        //     steps {
        //         sh 'docker exec pipeline sh -c "dagster asset materialize -m pipeline --select \\"*\\""'
        //     }
        // }
        // stage("Feast Materialization") {
        //     steps {
        //         sh 'docker exec mtl_pipeline sh -c "dagster job execute -m mtl_pipeline"'
        //     }
        // }
        // stage("Training Pipeline") {
        //     steps {
        //         sh 'docker exec training_pipeline sh -c "dagster asset materialize -m training_pipeline --select \\"*\\""'
        //     }
        // }
    }
}
