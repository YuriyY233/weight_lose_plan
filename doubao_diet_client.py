import requests
import os
from datetime import datetime, timedelta
from volcenginesdkarkruntime import Ark

class DoubaoDietClient:
    def __init__(self):
        self.api_key = os.getenv("DOUBAO_API_KEY")
        self.secret_key = os.getenv("DOUBAO_SECRET_KEY")
        self.base_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        self.token = None
        self.token_expire = None

    def _get_access_token(self):
        """获取API访问令牌[1,6](@ref)"""
        if self.token and self.token_expire > datetime.now():
            return self.token

        auth_url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
        }

        response = requests.get(auth_url, params=params)
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.token_expire = datetime.now() + timedelta(days=29)
            return self.token
        else:
            raise Exception(f"认证失败: {response.text}")

    def generate_diet_plan(self, user_profile):
        """生成个性化减肥计划[3,5](@ref)"""
        client = Ark(api_key=self.api_key)

        prompt = self._build_diet_prompt(user_profile)

        try:
            resp = client.chat.completions.create(
                # model="doubao-seed-1-6-lite-251015",
                model="deepseek-v3-2-251201",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                stream=True
            )
            yield from self._parse_diet_response(resp)
        except Exception as e:
            yield f'{{"error": "API调用失败: {str(e)}"}}'

    def _build_diet_prompt(self, profile):
        """构建减肥计划提示词[5](@ref)"""
        return f"""
请为以下用户生成一份详细的7天减肥计划。

用户信息：
- 年龄: {profile['age']}
- 性别: {profile['gender']}
- 当前体重: {profile['weight']}kg
- 目标体重: {profile['target_weight']}kg
- 身高: {profile['height']}cm
- 日常活动水平: {profile['activity_level']}

**输出要求**：
请直接返回一份排版精美的 Markdown 文档，不要返回 JSON 格式。文档应包含以下部分：

1. **整体建议**：
   - 每日热量目标
   - 饮水建议
   - 核心注意事项（列出3点）

2. **7天详细计划表**：
   请使用 **Markdown 表格** 展示每天的安排，表格列头如下：
   | 天数 | 早餐 | 午餐 | 晚餐 | 加餐 | 运动建议 |
   | :--- | :--- | :--- | :--- | :--- | :--- |
   | 第1天 | ... | ... | ... | ... | ... |

   *注意：表格内容要具体，包含食物名称和大致分量。*

3. **鼓励寄语**：
   一句简短的鼓励话语。

请确保计划科学合理、可执行，适合该用户的身体状况。
"""

    def _parse_diet_response(self, response):
        """解析API响应，支持流式输出"""
        full_content = ""

        for chunk in response:
            if not chunk.choices:
                continue
                
            # 深度思考模型，且触发了深度思考，打印思维链内容
            if hasattr(chunk.choices[0].delta, 'reasoning_content') and chunk.choices[0].delta.reasoning_content:
                print(chunk.choices[0].delta.reasoning_content, end="")
                full_content=chunk.choices[0].delta.reasoning_content
            else:
                print(chunk.choices[0].delta.content, end="")
                full_content=chunk.choices[0].delta.content
            yield full_content

        # except Exception as e:
        #     return {"error": f"响应解析异常: {str(e)}", "raw_content": full_content}
