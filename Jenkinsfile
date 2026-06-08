pipeline {
  agent any

  options {
    timestamps()
    ansiColor('xterm')
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timeout(time: 15, unit: 'MINUTES')
    skipDefaultCheckout()
  }

  environment {
    AWS_DEFAULT_REGION = 'us-east-1'
    STACK              = 'todo-list-aws-staging'
    REPO_PATH          = 'github.com/fedefdz/unir-todo-list-aws.git'
  }

  stages {

    stage('Get Code') {
      steps {
        cleanWs()
        checkout scm
        sh '''
          whoami
          hostname
          echo $WORKSPACE
          git log -1 --oneline
        '''
      }
    }

    stage('Static') {
      parallel {
        stage('Flake8') {
          steps {
            sh '''
              flake8 --format=pylint --exit-zero --output-file=flake8.log src/
              cat flake8.log
            '''
          }
        }
        stage('Bandit') {
          steps {
            sh '''
              bandit --exit-zero -r src/ -f txt -o bandit.log
              cat bandit.log
            '''
          }
        }
      }
    }

    stage('Deploy Staging') {
      steps {
        sh '''
          sam build
          sam validate
          sam deploy --config-env staging
        '''
      }
    }

    stage('REST Tests') {
      steps {
        sh '''
          API=$(aws cloudformation describe-stacks --stack-name $STACK \
            --query 'Stacks[0].Outputs[?OutputKey==`BaseUrlApi`].OutputValue' --output text)
          echo "API: $API"
          BASE_URL="$API" pytest -v test/integration/todoApiTest.py --junitxml=result-rest.xml
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'result-rest.xml'
        }
      }
    }

    stage('Merge to master') {
      steps {
        withCredentials([usernamePassword(
            credentialsId: 'github-pat',
            usernameVariable: 'GH_USER',
            passwordVariable: 'GH_TOKEN')]) {
          sh '''
            git config user.email "jenkins@unir.edu"
            git config user.name  "Jenkins CI"
            git fetch origin master
            git checkout -B master origin/master
            git merge --no-ff origin/develop -m "auto-merge develop -> master (Jenkins #$BUILD_NUMBER)"
            git push "https://${GH_USER}:${GH_TOKEN}@${REPO_PATH}" master
          '''
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
