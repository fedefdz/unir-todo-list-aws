pipeline {
  agent any

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timeout(time: 15, unit: 'MINUTES')
    skipDefaultCheckout()
  }

  environment {
    AWS_DEFAULT_REGION = 'us-east-1'
    STACK              = 'todo-list-aws-production'
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
          curl -fsSL -o samconfig.toml \
            https://raw.githubusercontent.com/fedefdz/unir-todo-list-aws-config/production/samconfig.toml
          head samconfig.toml
        '''
      }
    }

    stage('Deploy Production') {
      steps {
        sh '''
          sam build
          sam validate
          sam deploy --config-env production
        '''
      }
    }

    stage('Rest Test') {
      steps {
        sh '''
          API=$(aws cloudformation describe-stacks --stack-name $STACK \
            --query 'Stacks[0].Outputs[?OutputKey==`BaseUrlApi`].OutputValue' --output text)
          echo "API: $API"
          BASE_URL="$API" pytest -v \
            test/integration/todoApiReadOnlyTest.py \
            --junitxml=result-rest.xml
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'result-rest.xml'
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
