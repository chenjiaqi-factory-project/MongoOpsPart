import random
import datetime


# 随机生成唯一编码
def create_random_hash():
    nowtime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    hash_code = hash(nowtime)
    # 绝对值处理
    if hash_code < 0 :
        hash_code = str(abs(hash_code))
    else:
        hash_code = str(hash_code)
    # 再添加随机位确保哈希值不重复
    seed = "abcdef"
    title = ""
    for _ in range(6):
        title = title + random.choice(seed)
    return str(title + hash_code)


# 生成记录唯一编码
def create_rec_hash():
    return "rec" + create_random_hash()

