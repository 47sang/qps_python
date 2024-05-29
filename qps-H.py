import re
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime

# 定义Nginx日志格式的正则表达式
log_pattern = re.compile(r'(\d+.\d+.\d+.\d+)\s-\s-\s\[(.+)\]\s"(\w+)\s?(.+)?\s?.*"\s(\d+)\s(\d+)\s"(.+)"\s"(.+)"')


def parse_log_line(line):
    """解析单行Nginx日志"""

    match = log_pattern.match(line)
    if match:
        ip, date, method, url, status_code, bytes_sent, referer, user_agent = match.groups()

        # timestamp时间戳的格式为 :
        # 17/May/2024:14:35:05
        # 截取为 :
        # 17/May/2024:14:35

        # 按照时统计数据
        timestamp = date.split()[0][12:-6]

        return timestamp, method, url, status_code
    return None


def analyze_qps(log_file):
    """分析Nginx日志中每秒钟的QPS"""
    requests_per_second = defaultdict(int)
    data = []  # 创建一个空列表来存储数据
    with open(log_file, 'r') as f:
        for line in f:
            log_entry = parse_log_line(line)
            if log_entry:
                timestamp, method, url, status_code = log_entry
                requests_per_second[timestamp] += 1

    # 将解析的数据存入数组中
    for timestamp, count in sorted(requests_per_second.items()):
        data.append([timestamp, count])

    return data


data = analyze_qps('access-2024-05-28.log')

# 绘制二维数据
timestamps, counts = zip(*data)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置窗口大小
plt.figure(figsize=(25, 6))
# 设置折线图左右内边距
plt.margins(x=0)

# 按照时间分组显示数据,针对分钟或秒效果好
plt.plot(timestamps, counts)

plt.xticks(rotation=45)

plt.xlabel('时间')
plt.ylabel('请求数')

plt.title('每小时请求统计图')
# 调整内边距
plt.subplots_adjust(left=0.03, right=0.99, top=0.95, bottom=0.1)
plt.show()
