import tiktoken
import secrets
import string

def num_tokens_from_string(string: str, model_name: str = 'gpt-3.5-turbo-16k') -> int:
    """
    计算字符串的token数量, OpenAI GPT-3.5 Turbo 16k模型
    :param string:
    :param model_name:
    :return:
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == '__main__':
    print(num_tokens_from_string("""
    李晓波说：建议国家在 WTO规则之 内，将出口 
不锈钢材及深加工制品的出口退税率提高到 17％， ◆邢钢进军不锈钢和特殊钢盘条(线材)产品领域 
使中国钢铁企业与国外企业平等竞争，提升在国际 西门子冶金技术部与邢台钢铁有限责任公司( 
市场上的竞争力。 邢钢)日前签署合同，负责为一个 50吨容量的 AOD 
“优势企业并购落后企业和困难企业，强强联 不锈钢转炉、一个相同容量的钢包炉以及一个 4流 
合和上下游一体化经营，提高产业集中度和资源配 方坯连铸机设计提供关键设备。这些设备是位于河 
置效率时，既要积极，又要稳妥，谨防 ‘背包袱 ’。” 北省邢台市的一个新生产设施的组成部分。邢钢将"""""))