pipeline {
    agent any

    environment {
        ALLURE_RESULTS = 'report/temp'
        ALLURE_REPORT = 'report/allureReport'
    }

    stages {
        stage('Init Extract File') {
            steps {
                sh '''
                mkdir -p extract
                echo "cookie: null" > extract/extract.yaml
                '''
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/13039797018/Test-Automation-Framework.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                if command -v uv &> /dev/null
                then
                    uv sync
                else
                    pip install -r requirements.txt || true
                fi

                # ✅ 确保 Jenkins 环境安装 pytest & allure-pytest
                pip install pytest allure-pytest || true
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                # ✅ 如果存在虚拟环境，则先激活
                if [ -d ".venv" ]; then
                    . .venv/bin/activate
                fi

                # ✅ 使用 python3 -m pytest 确保可执行
                python3 -m pytest --alluredir=${ALLURE_RESULTS}
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate ${ALLURE_RESULTS} -o ${ALLURE_REPORT} --clean'
            }
        }
    }

    post {
        always {
            allure includeProperties: true, results: [[path: 'report/temp']]
        }

        success {
            emailext(
                subject: "✅ 接口自动化测试成功 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>🎉 测试通过！</h2>
                    <p>项目：${env.JOB_NAME}</p>
                    <p>构建编号：#${env.BUILD_NUMBER}</p>
                    <p>报告链接：<a href="${env.BUILD_URL}allure">点击查看 Allure 报告</a></p>
                """,
                mimeType: 'text/html',
                to: "13039797018@163.com"
            )
        }

        failure {
            emailext(
                subject: "❌ 接口自动化测试失败 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>❌ 构建失败！</h2>
                    <p>项目：${env.JOB_NAME}</p>
                    <p>构建编号：#${env.BUILD_NUMBER}</p>
                    <p>控制台日志：<a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></p>
                """,
                mimeType: 'text/html',
                to: "13039797018@163.com"
            )
        }
    }
}
