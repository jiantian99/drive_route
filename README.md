# 每日通勤时间通知

这个脚本通过百度地图API获取路线规划信息，并在通勤时间超过阈值时将结果发送到企业微信。它可以从环境变量中读取关键信息，并支持定时运行。

## 功能

- **路线规划**: 使用百度地图API获取起点到终点的驾车路线信息，包括距离、时间和红绿灯数。
- **智能通知**: 仅在通勤时间超过设定阈值时发送企业微信通知。
- **节假日判断**: 支持节假日跳过模式，可以在节假日自动跳过执行。
- **灵活配置**: 所有关键参数都可通过环境变量配置。

## 使用步骤

### 1. 获取百度地图API密钥

1. 访问[百度地图开放平台](https://lbsyun.baidu.com/)并注册账号。
2. 创建一个应用并获取API密钥（`ak`）。

### 2. 获取企业微信Webhook Key

1. 登录企业微信管理后台。
2. 创建一个群聊机器人并获取Webhook Key。

### 3. 设置环境变量

在GitHub仓库的`Settings -> Secrets and variables -> Actions`中，添加以下环境变量：

必需变量（需要在 Secrets 中设置）：
- `BAIDU_MAP_AK`: 百度地图API密钥
- `WECHAT_WEBHOOK_KEY`: 企业微信机器人的Webhook Key
- `ROUTE_ORIGIN`: 起点的经纬度，格式为`纬度,经度`
- `ROUTE_DESTINATION`: 终点的经纬度，格式为`纬度,经度`

可选变量（需要在 Secrets 中设置）：
- `ROUTE_WAYPOINTS`: 途径点的经纬度，多个途径点用竖线`|`分隔

配置参数（在 workflow 文件中直接设置）：
- `RUN_MODE`: 运行模式
  - `0`: 默认模式，每天执行
  - `1`: 节假日跳过模式，工作日执行（当前设置）
- `DURATION_THRESHOLD`: 通勤时间阈值（分钟）
  - 设置为40分钟，仅当预计通勤时间超过此阈值时才发送通知

### 4. 配置GitHub Actions

工作流配置文件`.github/workflows/run_route_plan.yml`已包含所有必要的设置，包括：
- 定时任务配置
- 环境变量设置
- 运行模式和阈值设置

### 5. 运行说明

- **定时运行**: 脚本将根据GitHub Actions的定时任务自动运行。
- **手动运行**: 在GitHub仓库的`Actions`页面，可以手动触发工作流。
- **节假日处理**: 当`RUN_MODE=1`时，脚本会在节假日自动跳过执行。
- **通知控制**: 当设置了`DURATION_THRESHOLD`时，只有通勤时间超过阈值才会发送通知。

## 输出示例

当通勤时间超过阈值时，企业微信将收到类似以下消息：

```
今日通勤信息
时间：45 分钟
距离：15.5 公里
灯数：12
```

## 依赖

- Python 3.9+
- requests==2.32.3
- pytz==2024.1

## 代码结构

主要功能模块：
- `get_route_plan`: 获取百度地图路线规划信息
- `send_wx_message`: 发送企业微信通知
- `is_holiday`: 判断是否为节假日
- `get_env_config`: 获取环境变量配置
- `format_route_message`: 格式化通知消息

## 许可证

本项目采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 贡献

欢迎提交Issue和Pull Request。