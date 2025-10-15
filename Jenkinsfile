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
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                if [ -d ".venv" ]; then
                    . .venv/bin/activate
                fi
                python3 -m pytest --alluredir=${ALLURE_RESULTS}
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo "✅ Skip manual allure generation; Jenkins Allure plugin will handle it."
            }
        }

        // ✅ 自动安装 zip 并压缩报告
        stage('Archive Report') {
            steps {
                sh '''
                # 自动安装 zip（WSL/Ubuntu）
                if ! command -v zip &> /dev/null; then
                    echo "🧩 Installing zip..."
                    sudo apt-get update -y && sudo apt-get install -y zip
                fi

                cd report
                if [ -d "allureReport" ]; then
                    zip -r allure-report.zip allureReport > /dev/null
                    echo "✅ Allure report successfully compressed."
                else
                    echo "⚠️ allureReport directory not found. Skipping compression."
                fi
                '''
                archiveArtifacts artifacts: 'report/allure-report.zip', fingerprint: true
            }
        }
    }

    post {
        always {
            allure includeProperties: true, results: [[path: 'report/temp']]
        }

        success {
            echo "✅ 所有测试均通过，标记为 SUCCESS"
            script { currentBuild.result = 'SUCCESS' }

            emailext(
                subject: "✅ 接口自动化测试成功 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>🎉 所有接口测试通过！</h2>
                    <p>项目名称：${env.JOB_NAME}</p>
                    <p>构建编号：#${env.BUILD_NUMBER}</p>
                    <p>报告链接：<a href="${env.BUILD_URL}allure">点击查看 Allure 报告</a></p>
                    <p>如需离线查看，可下载附件：<b>allure-report.zip</b></p>
                """,
                mimeType: 'text/html',
                to: "13039797018@163.com",
                attachmentsPattern: "report/allure-report.zip"
            )
        }

        failure {
            emailext(
                subject: "❌ 接口自动化测试失败 - ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                    <h2>❌ 构建失败！</h2>
                    <p>项目名称：${env.JOB_NAME}</p>
                    <p>构建编号：#${env.BUILD_NUMBER}</p>
                    <p>控制台日志：<a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></p>
                """,
                mimeType: 'text/html',
                to: "13039797018@163.com"
            )
        }
    }
}
