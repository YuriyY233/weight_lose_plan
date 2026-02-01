from flask import Flask, render_template, request, jsonify, Response, stream_with_context
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from doubao_diet_client import DoubaoDietClient

app = Flask(__name__)
diet_client = DoubaoDietClient()

# 存储用户计划（生产环境应使用数据库）
USER_PLANS_FILE = "user_plans.json"

def load_user_plans():
    """加载用户计划数据"""
    if os.path.exists(USER_PLANS_FILE):
        with open(USER_PLANS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_user_plans(plans):
    """保存用户计划数据"""
    with open(USER_PLANS_FILE, 'w', encoding='utf-8') as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """主页 - 减肥计划生成器[2](@ref)"""
    return render_template('index.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    """生成减肥计划API端点"""
    user_data = request.json
    
    # 基本数据验证
    required_fields = ['age', 'gender', 'weight', 'target_weight', 'height']
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            return jsonify({"error": f"缺少必要字段: {field}"}), 400
    
    return Response(stream_with_context(diet_client.generate_diet_plan(user_data)), mimetype='text/plain')

@app.route('/daily_schedule/<date>')
def get_daily_schedule(date):
    """获取特定日期的详细安排[2](@ref)"""
    user_id = request.args.get('user_id', 'default_user')
    plans = load_user_plans()
    
    if user_id not in plans:
        return jsonify({"error": "用户计划不存在"}), 404
    
    # 这里可以扩展为根据日期返回特定天的计划
    return jsonify(plans[user_id]['plan'])

if __name__ == '__main__':
    app.run(debug=True, port=5000)