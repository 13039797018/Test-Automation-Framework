pipeline {
    agent any

    environment {
        ALLURE_RESULTS = 'report/temp'
        ALLURE_REPORT = 'report/allureReport'
    }

    stages {
        stage('Checkout') {
            steps {
                // ✅ 修复：指定正确的分支 main（原先默认找 master 报错）
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
                sh 'python run.py'
            }
        }

        stage('Generate Allure Report') {
            steps {
                // ✅ allure CLI 会在 Jenkins 全局工具配置中自动安装
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
            // ✅ Jenkins allure 插件自动发布报告
            allure includeProperties: true, results: [[path: 'report/temp']]
        }
    }
}
