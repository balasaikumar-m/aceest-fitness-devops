pipeline {
    agent any
    options {
        timestamps()
        disableConcurrentBuilds()
    }
    triggers {
        pollSCM('H/5 * * * *')
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Clean Python Build') {
            steps {
                sh '''
                    rm -rf .venv
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install -r requirements-dev.txt
                    .venv/bin/python -m compileall -q app.py tests
                '''
            }
        }
        stage('Unit Tests and Coverage') {
            steps {
                sh '''
                    .venv/bin/coverage run -m pytest -v
                    .venv/bin/coverage xml -o coverage.xml
                    .venv/bin/coverage report -m
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t aceest-fitness:jenkins-${BUILD_NUMBER} .'
            }
        }
        stage('Containerized Tests') {
            steps {
                sh 'docker run --rm aceest-fitness:jenkins-${BUILD_NUMBER} python -m pytest -v'
            }
        }
        stage('SonarQube Analysis') {
    steps {
        script {
            // 1. Fetch the absolute folder location where Jenkins downloads the tool
            def scannerHome = tool 'SonarScanner'
            
            // 2. Wrap it with your SonarQube system credentials config
            withSonarQubeEnv('SonarQube') { 
                // 3. CRUCIAL: Point directly to the binary inside that installation folder
                sh "${scannerHome}/bin/sonar-scanner -Dproject.settings=sonar-project.properties -Dsonar.python.coverage.reportPaths=coverage.xml"
            }
        }
    }
}
        stage('SonarQube Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
    post {
        success { echo 'Build, tests, Docker and SonarQube quality gate passed.' }
        failure { echo 'Pipeline failed. Review the stage logs.' }
        always { echo 'Jenkins pipeline completed.' }
    }
}
