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
                // ✅ 关键修改：直接调用虚拟环境中的 python
                sh '.venv/bin/python run.py || true'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate ${ALLURE_RESULTS} -o ${ALLURE_REPORT} --clean'
            }
        }

        stage('Send DingTalk Notification') {
            steps {
                script {
                    def xml = readFile('report/results.xml')
                    def total = (xml =~ /tests="(\\d+)"/)[0][1]
                    def failed = (xml =~ /failures="(\\d+)"/)[0][1]
                    def time = (xml =~ /time="([\\d.]+)"/)[0][1]
                    def success = (1 - failed.toInteger() / total.toInteger()) * 100

                    sh """
                    curl 'https://oapi.dingtalk.com/robot/send?access_token=你的钉钉token' \
                        -H 'Content-Type: application/json' \
                        -d '{
                              "msgtype": "text",
                              "text": {"content": "接口自动化测试完成 ✅\\n总用例: ${total}\\n失败: ${failed}\\n成功率: ${success.round(2)}%\\n耗时: ${time}s"}
                            }'
                    """
                }
            }
        }
    }

    post {
        always {
            allure includeProperties: true, results: [[path: 'report/temp']]
        }

        // ✅ 构建成功时发邮件
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

        // ❌ 构建失败时发邮件
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
