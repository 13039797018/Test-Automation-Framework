import yaml
import traceback
import os

from common.recordlog import logs
from conf.operationConfig import OperationConfig
from conf.setting import FILE_PATH


def get_testcase_yaml(file):
    testcase_list = []
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if len(data) <= 1:
                yam_data = data[0]
                base_info = yam_data.get('baseInfo')
                for ts in yam_data.get('testCase'):
                    param = [base_info, ts]
                    testcase_list.append(param)
                return testcase_list
            else:
                return data
    except UnicodeDecodeError:
        logs.error(f"[{file}]文件编码格式错误，--尝试使用utf-8编码解码YAML文件时发生了错误，请确保你的yaml文件是UTF-8格式！")
    except FileNotFoundError:
        logs.error(f'[{file}]文件未找到，请检查路径是否正确')
    except Exception as e:
        logs.error(f'获取【{file}】文件数据时出现未知错误: {str(e)}')


class ReadYamlData:
    """读写接口的YAML格式测试数据"""

    def __init__(self, yaml_file=None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            pass
        self.conf = OperationConfig()
        self.yaml_data = None

    @property
    def get_yaml_data(self):
        """
        获取测试用例yaml数据
        :param file: YAML文件
        :return: 返回list
        """
        # Loader=yaml.FullLoader表示加载完整的YAML语言，避免任意代码执行，无此参数控制台报Warning
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                self.yaml_data = yaml.safe_load(f)
                return self.yaml_data
        except Exception:
            logs.error(str(traceback.format_exc()))

    def write_yaml_data(self, value):
        """
        写入数据需为dict，allow_unicode=True表示写入中文，sort_keys按顺序写入
        写入YAML文件数据,主要用于接口关联
        :param value: 写入数据，必须用dict
        :return:
        """
        file_path = FILE_PATH['EXTRACT']

        # ✅ 若文件不存在则创建
        if not os.path.exists(file_path):
            logs.info(f"extract.yaml 不存在，自动创建：{file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump({}, f, allow_unicode=True)

        try:
            # ✅ 先读取原内容
            with open(file_path, 'r', encoding='utf-8') as f:
                old_data = yaml.safe_load(f) or {}

            # ✅ 合并更新
            if isinstance(value, dict):
                old_data.update(value)
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(old_data, f, allow_unicode=True, sort_keys=False)
                logs.info(f"✅ 已写入 extract.yaml: {value}")
            else:
                logs.error('写入 extract.yaml 的数据必须为 dict 格式')

        except Exception as e:
            logs.error(f"写入 extract.yaml 失败: {e}")

    def clear_yaml_data(self):
        """
        清空extract.yaml文件数据
        :param filename: yaml文件名
        :return:
        """
        with open(FILE_PATH['EXTRACT'], 'w') as f:
            f.truncate()

    def get_extract_yaml(self, node_name, second_node_name=None):
        """
        用于读取接口提取的变量值
        """
        file_path = FILE_PATH['EXTRACT']

        # ✅ 文件不存在则自动创建空文件
        if not os.path.exists(file_path):
            logs.warning("extract.yaml 不存在，自动创建空文件")
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump({}, f)

        try:
            with open(file_path, 'r', encoding='utf-8') as rf:
                ext_data = yaml.safe_load(rf) or {}

                # ✅ 一级 key
                if second_node_name is None:
                    value = ext_data.get(node_name)
                else:
                    value = ext_data.get(node_name, {}).get(second_node_name)

                if value is None:
                    logs.warning(f"【extract.yaml】未找到键：{node_name} (可能还未写入)")
                return value

        except Exception as e:
            logs.error(f"读取 extract.yaml 出错: {e}")
            return None

    def get_testCase_baseInfo(self, case_info):
        """
        获取testcase yaml文件的baseInfo数据
        :param case_info: yaml数据，dict类型
        :return:
        """
        pass

    def get_method(self):
        """
        :param self:
        :return:
        """
        yal_data = self.get_yaml_data()
        metd = yal_data[0].get('method')
        return metd

    def get_request_parame(self):
        """
        获取yaml测试数据中的请求参数
        :return:
        """
        data_list = []
        yaml_data = self.get_yaml_data()
        del yaml_data[0]
        for da in yaml_data:
            data_list.append(da)
        return data_list
