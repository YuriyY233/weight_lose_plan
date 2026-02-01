# 智能减肥计划生成器 (Lose Weight AI)

这是一个基于 Flask 和 AI 大模型的智能减肥计划生成应用。它能够根据用户的年龄、性别、体重、身高、目标体重和活动水平，实时生成个性化的减肥饮食计划。

## 功能特性

- **个性化定制**：基于用户身体数据量身定制科学的饮食方案。
- **AI 驱动**：集成火山引擎 (Volcengine) Ark Runtime，支持豆包/DeepSeek 等先进大模型。
- **流式响应**：采用 Server-Sent Events (SSE) 风格的流式输出技术，实现实时打字机效果，大幅降低用户等待焦虑。
- **Markdown 渲染**：前端集成 `marked.js`，支持表格、列表等富文本的实时渲染与展示。

## 快速开始

### 1. 环境准备

确保您的系统已安装 Python 3.8 或更高版本。

建议创建并激活虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate

# 激活虚拟环境 (Windows)
venv\Scripts\activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录下创建一个 `.env` 文件，并配置您的 API Key：

```ini
# 火山引擎 (Volcengine) / 豆包 API 配置
DOUBAO_API_KEY=your_api_key_here
```

> **注意**：请确保您已在火山引擎控制台开通了相应的模型服务（如 DeepSeek 或 豆包），并获取了有效的 API Key。

### 4. 运行应用

```bash
python app.py
```

启动成功后，打开浏览器访问：[http://127.0.0.1:5000](http://127.0.0.1:5000)

## 使用指南

1.  在网页表单中输入您的个人信息（年龄、性别、身高、体重等）。
2.  点击“生成减肥计划”按钮。
3.  系统将立即开始生成，并在页面下方实时显示计划内容。
4.  生成的计划包含每日饮食建议、热量摄入分析等详细信息。

## 项目结构

```text
lose-weight-ai/
├── app.py                  # Flask 后端主程序，处理路由和请求
├── doubao_diet_client.py   # AI 客户端封装，负责调用大模型 API
├── requirements.txt        # Python 项目依赖
├── .env                    # 环境变量配置文件 (需手动创建)
└── templates/
    └── index.html          # 前端页面，包含 HTML/CSS/JS 逻辑
```

## 技术栈

- **后端**: Flask, Python
- **AI SDK**: volcenginesdkarkruntime (火山引擎 Ark Runtime)
- **前端**: HTML5, CSS3, JavaScript (Fetch API, ReadableStream)
- **工具库**: python-dotenv, marked.js
