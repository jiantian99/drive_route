import requests
import json
import os
from datetime import datetime
import pytz

def is_holiday():
    """
    检查今天是否是中国节假日（基于中国时区）
    :return: 是否为节假日的布尔值
    """
    # 使用中国时区获取当前日期
    china_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(china_tz)
    today = now.strftime('%Y-%m-%d')
    year = now.year
    
    # 使用 PublicHolidays 端点获取中国节假日
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/CN"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            holidays = response.json()
            # 检查今天是否在节假日列表中
            # 输出节假日信息并优化返回值
            if response.status_code == 200:
                holidays = response.json()
                is_holiday = any(holiday['date'] == today for holiday in holidays)
                if is_holiday:
                    print(f"今天({today})是节假日")
                else:
                    print(f"今天({today})是工作日")
                return is_holiday
            return any(holiday['date'] == today for holiday in holidays)
        else:
            print(f"节假日查询失败，状态码：{response.status_code}")
            return False
    except Exception as e:
        print(f"节假日查询出错：{str(e)}")
        return False

def get_route_plan(api_key, origin, destination, waypoints):
    """
    获取百度地图API的路线规划信息
    :param api_key: 百度地图API的密钥
    :param origin: 起点的经纬度，格式为"纬度,经度"
    :param destination:  终点的经纬度，格式为"纬度,经度"
    :param waypoints: 途径点的经纬度，多个途径点用竖线|分隔
    :return: 包含距离、时间和红绿灯数的字典，若请求失败则返回None
    """
    # 百度地图API的URL
    url = "https://api.map.baidu.com/direction/v2/driving"

    # 请求参数
    params = {
        "origin": origin,
        "destination": destination,
        "ak": api_key,
        "output": "json",
    }

    # 如果有途径点，添加到参数中
    if waypoints:
        params["waypoints"] = waypoints

    # 发送GET请求
    response = requests.get(url, params=params)
    result = response.json()

    # 解析结果
    if result["status"] == 0:
        route = result["result"]["routes"][0]
        distance = route["distance"] / 1000  # 转换为公里
        duration = route["duration"] / 60  # 转换为分钟

        # 获取红绿灯数
        traffic_lights = route["traffic_light"]

        return {
            "distance": round(distance, 1),
            "duration": int(duration),
            "traffic_lights": traffic_lights,
        }
    else:
        print("请求失败，错误码：", result["status"])
        return None


def send_wx_message(webhook_key, message):
    """
    发送消息到企业微信
    :param webhook_key: 企业微信机器人的Webhook Key
    :param message: 要发送的消息内容
    :return:
    """
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    # 构造消息体
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }

    # 发送POST请求
    headers = {"Content-Type": "application/json"}
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    # 检查是否发送成功
    if response.status_code == 200 and response.json()["errcode"] == 0:
        print("消息成功发送到企业微信！")
    else:
        print("消息发送失败，错误信息：", response.text)


def get_env_config():
    """
    获取环境变量配置
    :return: 配置字典
    """
    return {
        "run_mode": int(os.getenv("RUN_MODE", "0")),
        "ak": os.getenv("BAIDU_MAP_AK"),
        "webhook_key": os.getenv("WECHAT_WEBHOOK_KEY"),
        "origin": os.getenv("ROUTE_ORIGIN"),
        "destination": os.getenv("ROUTE_DESTINATION"),
        "waypoints": os.getenv("ROUTE_WAYPOINTS"),
        "duration_threshold": int(os.getenv("DURATION_THRESHOLD", "0"))
    }


def format_route_message(route_info):
    """
    格式化路线信息消息
    :param route_info: 路线信息字典
    :return: 格式化后的消息字符串
    """
    return (
        f"今日通勤信息\n"
        f"时间：{route_info['duration']} 分钟\n"
        f"距离：{route_info['distance']} 公里\n"
        f"灯数：{route_info['traffic_lights']}"
    )


if __name__ == "__main__":
    # 获取配置
    config = get_env_config()

    # 节假日检查
    if config["run_mode"] == 1 and is_holiday():
        print("今天是节假日，跳过执行")
        exit(0)

    # 获取路线规划信息
    route_info = get_route_plan(
        config["ak"],
        config["origin"],
        config["destination"],
        config["waypoints"]
    )

    if route_info:
        message = format_route_message(route_info)
        print(message)
        
        # 检查是否需要发送通知
        if route_info['duration'] > config["duration_threshold"]:
            send_wx_message(config["webhook_key"], message)
            print(f"通勤时间 {route_info['duration']} 分钟超过阈值 "
                  f"{config['duration_threshold']} 分钟，已发送通知")
        else:
            print(f"通勤时间 {route_info['duration']} 分钟未超过阈值 "
                  f"{config['duration_threshold']} 分钟，无需通知")
    else:
        message = "路线获取失败！"
        send_wx_message(config["webhook_key"], message)
