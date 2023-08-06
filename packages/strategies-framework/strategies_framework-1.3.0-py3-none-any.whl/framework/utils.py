import json


def file2dict(path):
    """
    从文件读取配置信息转字典
    :param path: 配置文件路径
    :return:
    """
    try:
        # 读取配置文件
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(e.args)


def select_pan_type(code: str) -> str:
    """
    判断内外盘
    :param code:NYMEX_F_CL_2007
    :return:
    """
    contratelist = str(code).split('_')
    if contratelist[0].upper() in ['SHFE', 'CFFEX', 'DCE', 'CZCE']:
        return 'in'  # 内盘
    else:
        return 'out'  # 外盘


def isKtypeRight(ktype):
    if ktype in ['1Min', '5Min', '15Min', '30Min', '60Min', 'klDay', 'klWeek']:
        return True
    return False
