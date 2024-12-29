class CourseSelectionSystem:
    def __init__(self):
        # 初始化课程数据，包含课程名称、类型（必修/选修）、描述和是否已选
        self.courses = [
            {"name": "Mathematics", "type": "必修", "description": "基础数学课程，涵盖代数、几何等内容。",
             "selected": False},
            {"name": "English", "type": "必修", "description": "英语语言学习课程，重点提升听说读写能力。",
             "selected": False},
            {"name": "History", "type": "选修", "description": "世界历史课程，探讨各国历史发展及重要事件。",
             "selected": False},
            {"name": "Art", "type": "选修", "description": "艺术课程，涵盖美术、音乐等艺术表现形式。", "selected": False},
            {"name": "Computer Science", "type": "必修", "description": "计算机科学基础课程，涵盖编程、数据结构等内容。",
             "selected": False},
            {"name": "Music", "type": "选修", "description": "音乐课程，学习音乐理论与实践技能。", "selected": False}
        ]

    # 查询功能，按课程类型筛选
    def query_courses(self, course_type=None):
        results = []
        if course_type == None:
            return self.courses
        for course in self.courses:
            if course["type"] == course_type:
                results.append(course)
        return results

    # 选课功能，返回选课结果
    def select_course(self, course_name):
        for course in self.courses:
            if course["name"] == course_name:
                if course["selected"]:
                    return f"您已经选择了 {course_name}。"
                else:
                    course["selected"] = True
                    return f"成功选择课程 {course_name}！"
        return f"课程 {course_name} 不存在。"

    # 删除选课功能，返回删除结果
    def remove_course(self, course_name):
        for course in self.courses:
            if course["name"] == course_name:
                if not course["selected"]:
                    return f"您没有选择课程 {course_name}，无法删除。"
                else:
                    course["selected"] = False
                    return f"成功删除课程 {course_name}。"
        return f"课程 {course_name} 不存在。"



    def selcted_courses(self):
        # 返回已选课程
        return [course for course in self.courses if course["selected"]]

# 测试用例
if __name__ == "__main__":
    system = CourseSelectionSystem()

    # 显示所有课程
    system.show_courses()

    # 查询选修课程
    print("\n查询选修课程:")
    selected_courses = system.query_courses("选修")
    for course in selected_courses:
        print(course["name"])
        print(f"描述: {course['description']}")
        print()

    # 选课
    print("\n选课：")
    print(system.select_course("Art"))
    print(system.select_course("Mathematics"))

    # 再次显示所有课程状态
    system.show_courses()

    # 删除选课
    print("\n删除选课：")
    print(system.remove_course("Art"))
    print(system.remove_course("Mathematics"))

    # 最终显示课程状态
    system.show_courses()
