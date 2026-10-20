# 智能旅行助手 🌍✈️

AI 驱动的个性化旅行规划 Web 应用。用户在网页上输入目的地、出行日期与偏好，系统通过多智能体协作自动生成包含每日行程、景点、酒店、三餐、天气与预算的完整旅行计划，并在高德地图上可视化展示。

## ✨ 功能特点

- 🤖 **多智能体协作规划**: 四个专职 Agent 分工完成景点搜索、天气查询、酒店推荐与行程整合
- 🗺️ **高德地图集成**: 通过 MCP 协议接入高德地图服务,支持景点搜索、天气查询、路线规划
- 🧠 **大模型工具调用**: Agent 自主决策调用地图工具获取实时数据,避免编造景点信息
- 🎨 **现代化前端**: Vue3 + TypeScript + Vite + Ant Design Vue,响应式设计
- 📱 **完整行程**: 包含每日景点、三餐、酒店、天气、预算与旅行建议

## 🏗️ 技术栈

### 后端
- **Agent框架**: HelloAgents (SimpleAgent + MCPTool)
- **Web框架**: FastAPI + Uvicorn
- **数据模型**: Pydantic v2
- **LLM**: DeepSeek (OpenAI 兼容接口,可切换任意兼容服务商)
- **工具协议**: MCP (amap-mcp-server)

### 前端
- **框架**: Vue 3 + TypeScript
- **构建工具**: Vite
- **UI组件库**: Ant Design Vue
- **地图服务**: 高德地图 JavaScript API
- **HTTP客户端**: Axios

## 📁 项目结构

```
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── agents/            # 多智能体实现
│   │   ├── api/               # FastAPI 路由
│   │   ├── services/          # LLM / 地图 / 图片服务
│   │   ├── models/            # Pydantic 数据模型
│   │   └── config.py          # 配置管理
│   ├── requirements.txt
│   └── .env.example
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── services/          # API 封装
│   │   ├── types/             # TypeScript 类型
│   │   └── views/             # 表单页 / 结果页
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 🚀 快速开始

### 前提条件

- Python 3.10+
- Node.js 16+
- 高德地图 API 密钥 (Web服务 与 Web端JS API 各一个)
- LLM API 密钥 (DeepSeek / 硅基流动等)

### 后端启动

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# 编辑 .env, 填入 LLM 与高德密钥
python run.py                # 访问 http://localhost:8000/docs
```

### 前端启动

```bash
cd frontend
npm install
# 编辑 .env, 填入高德 Web 服务 Key 与 JS Key
npm run dev                  # 访问 http://localhost:5173
```

## 🔧 核心实现

### 多智能体协作

系统包含四个 Agent,以流水线方式协作:

1. **景点搜索专家**: 调用高德 POI 搜索接口,获取真实景点数据
2. **天气查询专家**: 调用高德天气接口,获取出行期间天气
3. **酒店推荐专家**: 调用高德搜索接口,推荐符合预算的酒店
4. **行程规划专家**: 整合前三者数据,输出结构化 JSON 行程

```python
from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool

# 高德地图 MCP 工具(四个 Agent 共享)
amap_tool = MCPTool(
    name="amap",
    server_command=["uvx", "amap-mcp-server"],
    env={"AMAP_MAPS_API_KEY": settings.amap_api_key},
    auto_expand=True
)

# 景点搜索 Agent
attraction_agent = SimpleAgent(
    name="景点搜索专家",
    llm=HelloAgentsLLM(),
    system_prompt=ATTRACTION_AGENT_PROMPT
)
attraction_agent.add_tool(amap_tool)
```

### 工具调用协议

Agent 通过文本协议 `[TOOL_CALL:工具名:参数]` 自主决定调用工具,框架解析后执行并回填真实数据:

```
[TOOL_CALL:amap_maps_text_search:keywords=历史文化,city=北京]
```

## 📄 API 文档

启动后端后访问 `http://localhost:8000/docs` 查看交互式 API 文档。

主要端点:
- `POST /api/trip/plan` - 生成旅行计划
- `GET /api/map/poi` - 搜索 POI
- `GET /api/map/weather` - 查询天气
- `POST /api/map/route` - 规划路线

## 📝 使用指南

1. 在首页填写目的地、日期、偏好、预算等信息
2. 点击"生成旅行计划"
3. 系统依次调用各 Agent 获取景点、天气、酒店数据
4. 查看结果页:每日行程、地图标记、天气预报、餐饮与预算明细

---

**智能旅行助手** - 基于多智能体架构的 AI 旅行规划应用
