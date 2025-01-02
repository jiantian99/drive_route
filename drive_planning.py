import requests
import json
import os


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


if __name__ == "__main__":
    # 从环境变量中获取百度地图API密钥和企业微信Webhook Key
    ak = os.getenv("BAIDU_MAP_AK")
    webhook_key = os.getenv("WECHAT_WEBHOOK_KEY")

    # 从环境变量中获取起点、终点和途径点的经纬度
    # 起点
    origin = os.getenv("ROUTE_ORIGIN")
    # 终点
    destination = os.getenv("ROUTE_DESTINATION")
    # 设置途径点（经纬度，多个途径点用竖线|分隔）
    waypoints = os.getenv("ROUTE_WAYPOINTS")

    # 获取路线规划信息
    main_route_info = get_route_plan(ak, origin, destination, waypoints)

    if main_route_info:
        message = (
            f"环城路通勤\n"
            f"时间：{main_route_info['duration']} 分钟\n"
            f"距离：{main_route_info['distance']} 公里\n"
            f"灯数：{main_route_info['traffic_lights']}"
        )
        print(message)
        send_wx_message(webhook_key, message)
    else:
        # 如果路线获取失败，发送错误消息
        message = "路线获取失败！"
        send_wx_message(webhook_key, message)
