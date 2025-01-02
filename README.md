# 每日通勤时间通知

这个脚本通过百度地图API获取路线规划信息，并将结果发送到企业微信。它可以从环境变量中读取关键信息，并支持定时运行。

## 功能

- **路线规划**: 使用百度地图API获取起点到终点的驾车路线信息，包括距离、时间和红绿灯数。
- **企业微信通知**: 将路线规划结果发送到企业微信，方便及时查看。

## 使用步骤

### 1. 获取百度地图API密钥

1. 访问[百度地图开放平台](https://lbsyun.baidu.com/)并注册账号。
2. 创建一个应用并获取API密钥（`ak`）。

### 2. 获取企业微信Webhook Key

1. 登录企业微信管理后台。
2. 创建一个群聊机器人并获取Webhook Key。

### 3. 设置环境变量

在GitHub仓库的`Settings -> Secrets and variables -> Actions`中，添加以下环境变量：

- `BAIDU_MAP_AK`: 百度地图API密钥。
- `WECHAT_WEBHOOK_KEY`: 企业微信机器人的Webhook Key。
- `ROUTE_ORIGIN`: 起点的经纬度，格式为`纬度,经度`。
- `ROUTE_DESTINATION`: 终点的经纬度，格式为`纬度,经度`。
- `ROUTE_WAYPOINTS`: 途径点的经纬度，多个途径点用竖线`|`分隔（可选）。

### 4. 配置GitHub Actions

在仓库中创建`.github/workflows/run_script.yml`文件，内容如下：

```yaml
name: Run Route Plan Script

on:
  schedule:
    - cron: '0 8 * * *'  # 每天8点运行
  workflow_dispatch:  # 允许手动触发

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests

    - name: Run script
      env:
        BAIDU_MAP_AK: ${{ secrets.BAIDU_MAP_AK }}
        WECHAT_WEBHOOK_KEY: ${{ secrets.WECHAT_WEBHOOK_KEY }}
        ROUTE_ORIGIN: ${{ secrets.ROUTE_ORIGIN }}
        ROUTE_DESTINATION: ${{ secrets.ROUTE_DESTINATION }}
        ROUTE_WAYPOINTS: ${{ secrets.ROUTE_WAYPOINTS }}
      run: python main.py
```

### 5. 运行脚本

- **定时运行**: 脚本将根据GitHub Actions的定时任务自动运行。
- **手动运行**: 在GitHub仓库的`Actions`页面，手动触发工作流。

## 输出示例

脚本运行成功后，企业微信将收到类似以下消息：

```
今日通勤信息
时间：30 分钟
距离：15.5 公里
灯数：10
```

## 依赖

- Python 3.9+
- `requests`库

## 许可证

本项目采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 贡献

欢迎提交Issue和Pull Request。