# 每日通勤时间通知

这个脚本支持使用百度地图或高德地图 API 获取路线规划信息，并在通勤时间超过阈值时将结果发送到企业微信。它可以从环境变量中读取关键信息，并支持定时运行。

## 功能

- **多平台支持**: 支持百度地图和高德地图 API，可以灵活选择使用
- **路线规划**: 获取起点到终点的驾车路线信息，包括距离、时间和红绿灯数
- **智能通知**: 仅在通勤时间超过设定阈值时发送企业微信通知
- **节假日判断**: 支持节假日跳过模式，可以在节假日自动跳过执行
- **灵活配置**: 所有关键参数都可通过环境变量配置

## 使用步骤

### 1. 获取地图 API 密钥

选择以下任一方式：

#### 百度地图（推荐）
1. 访问[百度地图开放平台](https://lbsyun.baidu.com/)并注册账号
2. 创建一个应用并获取 API 密钥（`ak`）

#### 高德地图（备选）
1. 访问[高德地图开放平台](https://lbs.amap.com/)并注册账号
2. 创建一个应用并获取 API 密钥（`key`）

### 2. 获取企业微信 Webhook Key

1. 登录企业微信管理后台
2. 创建一个群聊机器人并获取 Webhook Key

### 3. 获取经纬度
1. 获取起点、终点、途径点（如需）经纬度，**注意**：不同地图API经纬度坐标系不一样
2. 类似网站[经纬度查询定位](http://jingweidu.757dy.com/)

### 4. 设置环境变量

在 GitHub 仓库的`Settings -> Secrets and variables -> Actions`中，添加以下环境变量：

必需变量（需要在 Secrets 中设置）：
- `WECHAT_WEBHOOK_KEY`: 企业微信机器人的 Webhook Key
- `ROUTE_ORIGIN`: 起点的经纬度，格式：百度地图`纬度,经度`，高德地图`经度，纬度`
- `ROUTE_DESTINATION`: 终点的经纬度，格式：百度地图`纬度,经度`，高德地图`经度，纬度`

地图 API 密钥（至少需要设置其中一个，如果都设置，优先使用百度）：
- `BAIDU_MAP_AK`: 百度地图 API 密钥
- `GAODE_MAP_AK`: 高德地图 API 密钥

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

## 代码结构

主要功能模块：
- `get_route_plan`: 获取路线规划信息（支持百度地图和高德地图）
- `get_route_plan_baidu`: 获取百度地图路线规划信息
- `get_route_plan_gaode`: 获取高德地图路线规划信息
- `send_wx_message`: 发送企业微信通知
- `is_holiday`: 判断是否为节假日
- `get_env_config`: 获取环境变量配置
- `format_route_message`: 格式化通知消息

## 依赖

- Python 3.9+
- requests==2.32.3
- pytz==2024.1

## 许可证

本项目采用MIT许可证。详情请参阅[LICENSE](LICENSE)文件。

## 贡献

欢迎提交Issue和Pull Request。