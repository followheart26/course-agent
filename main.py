import os
import json
import courseSelectSystem
from langchain.chat_models import *
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
os.environ["OPENAI_API_KEY"] = "None"
os.environ["OPENAI_API_BASE"] = "http://10.58.0.2:8000/v1"
model = ChatOpenAI(model="Qwen2.5-14B")


# 解析并执行操作
def execute_action(course_system, action_json):
    action = json.loads(action_json)
    action_type = action.get("action")

    if action_type == "查询课程":
        if(action.get("course_selected") == True):
            result = course_system.selcted_courses()
            return f"已选课程：\n" + "\n".join(
                [f"{course['name']} ({course['type']}) - {course['description']}" for course in result])
        course_type = action.get("course_type")
        result = course_system.query_courses(course_type)
        return f"查询结果：\n" + "\n".join(
            [f"{course['name']} ({course['type']}) - {course['description']}" for course in result])

    elif action_type == "选择课程":
        course_name = action.get("course_name")
        if not course_name:
            return "请选择有效的课程名称。"
        return course_system.select_course(course_name)

    elif action_type == "删除课程":
        course_name = action.get("course_name")
        if not course_name:
            return "请选择有效的课程名称。"
        return course_system.remove_course(course_name)

    else:
        return "无法识别的操作类型。"
def call_openai_api(user_input):
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template=
        """
            以下是一个选课系统，您可以查询、选课或删除课程：
    
            您可以输入类似以下的自然语言需求：
            1. 查询所有选修/必修课程
            2. 选课：选择“计算机科学”课程
            3. 删除课程：删除“英语”课程
            4. 查询已选课程
            用户输入：{user_input}
    
            请以 JSON 格式输出以下内容，无需输出其他内容！！！！：
            {{
                "action": "查询课程" | "选择课程" | "删除课程",
                "course_name": "课程名称" (可选),
                "course_type": "选修" | "必修" (可选)
                "course_description": "课程描述" (可选)
                "course_selected": True | False (可选)
            }}
    
            example:
            1. input: 查询所有课程
               output: {{"action": "查询课程"}}
            2. input: 选课：选择“计算机科学”课程
               output: {{"action": "选择课程", "course_name": "计算机科学"}}
            3. input: 删除课程：删除“英语”课程
               output: {{"action": "删除课程", "course_name": "英语"}}
            4. input: 查询所有选修课程
               output: {{"action": "查询课程", "course_type": "选修"}}
            5. input: 查询所有已选课程
                output: {{"action": "查询课程", "course_selected": true}}
        """
    )
    query_chain = LLMChain(llm=model, prompt=prompt_template)
    response = query_chain.run({"user_input": user_input})
    return response

if __name__ == "__main__":
    system = courseSelectSystem.CourseSelectionSystem()
    while True:
        print("=================================>")
        user_input = input("请输入您的需求（例如：查询所有选修课）：")
        if user_input.lower() in ["exit", "quit", "退出"]:
            print("退出选课系统。")
            break

        # 获取 OpenAI API 的响应
        action_json = call_openai_api(user_input)
        print(execute_action(system, action_json))
