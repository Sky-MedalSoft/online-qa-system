from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import User, Class, Student, Assignment, Submission

teacher = APIRouter()

# 定义班级创建和更新模型
class ClassCreate(BaseModel):
    name: str
    teacher_id: int  # 教师ID

class ClassUpdate(BaseModel):
    id: int
    name: str

# 定义学生创建和更新模型
class StudentCreate(BaseModel):
    username: str
    password: str
    class_id: int

class StudentUpdate(BaseModel):
    user_id: int  # 学生的用户ID
    username: str

# 定义作业创建模型
class AssignmentCreate(BaseModel):
    title: str
    content: str
    start_date: str  # YYYY-MM-DD
    end_date: str
    class_id: int

@teacher.get("/classes", summary="获取班级列表", description="获取由教师管理的班级列表。")
async def get_classes(teacher_id: int):
    classes = await Class.filter(teacher_id=teacher_id)
    return classes

@teacher.get("/students", summary="获取学生列表", description="根据班级ID获取班级中的学生列表。")
async def get_students(class_id: int):
    students = await Student.filter(class_id=class_id).prefetch_related('user')
    return [{"id": student.user.id, "username": student.user.username} for student in students]

@teacher.post("/class", summary="创建班级", description="创建新的班级。")
async def create_class(class_data: ClassCreate):
    new_class = Class(name=class_data.name, teacher_id=class_data.teacher_id)
    await new_class.save()
    return {"message": "班级创建成功"}

@teacher.put("/class", summary="更新班级", description="更新现有班级的信息。")
async def update_class(class_update: ClassUpdate):
    class_to_update = await Class.get_or_none(id=class_update.id)
    if not class_to_update:
        raise HTTPException(status_code=404, detail="班级未找到")

    class_to_update.name = class_update.name
    await class_to_update.save()
    return {"message": "班级更新成功"}

@teacher.delete("/class/{class_id}", summary="删除班级", description="根据班级ID删除班级。")
async def delete_class(class_id: int):
    class_to_delete = await Class.get_or_none(id=class_id)
    if not class_to_delete:
        raise HTTPException(status_code=404, detail="班级未找到")

    await class_to_delete.delete()
    return {"message": "班级删除成功"}

@teacher.post("/student", summary="创建学生", description="创建新的学生账户。")
async def create_student(student_data: StudentCreate):
    existing_student = await User.get_or_none(username=student_data.username)
    if existing_student:
        raise HTTPException(status_code=400, detail="学生已存在")

    new_user = User(username=student_data.username, password=student_data.password, role="student")
    await new_user.save()

    new_student = Student(user_id=new_user.id, class_id=student_data.class_id)  # 注意user_id
    await new_student.save()

    return {"message": "学生创建成功"}

@teacher.put("/student", summary="更新学生信息", description="更新现有学生的账户信息。")
async def update_student(student_update: StudentUpdate):
    # 获取学生对象
    student = await Student.get_or_none(user_id=student_update.user_id)  # 通过 user_id 获取学生

    if not student:
        raise HTTPException(status_code=404, detail="学生未找到")

    # 根据 user_id 获取用户对象
    user = await User.get_or_none(id=student.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新学生的用户名
    user.username = student_update.username
    await user.save()  # 保存用户信息

    return {"message": "学生信息更新成功"}

@teacher.delete("/student/{user_id}", summary="删除学生", description="根据用户ID删除学生账户。")
async def delete_student(user_id: int):
    # 根据 user_id 获取学生对象
    student = await Student.get_or_none(user_id=user_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生未找到")

    # 删除用户信息
    await User.filter(id=user_id).delete()  # 直接使用 User.filter() 删除用户

    # 删除学生记录
    await student.delete()  # 删除学生记录

    return {"message": "学生和相关账户删除成功"}


@teacher.post("/assignment", summary="发布作业", description="发布新的作业。(日期格式为YYYY-MM-DD)")
async def create_assignment(assignment_data: AssignmentCreate):
    new_assignment = Assignment(
        title=assignment_data.title,
        content=assignment_data.content,
        start_date=assignment_data.start_date,
        end_date=assignment_data.end_date,
        class_id=assignment_data.class_id
    )
    await new_assignment.save()
    return {"message": "作业发布成功"}

@teacher.get("/assignments", summary="获取已发布作业列表", description="获取教师发布的所有作业。")
async def get_assignments(teacher_id: int):
    classes = await Class.filter(teacher_id=teacher_id).values_list('id', flat=True)
    assignments = await Assignment.filter(class_id__in=classes)
    return [{
        "id": assignment.id,
        "title": assignment.title,
        "content": assignment.content,
        "start_date": assignment.start_date,
        "end_date": assignment.end_date,
    } for assignment in assignments]

@teacher.put("/assignment/{assignment_id}/cancel", summary="取消作业", description="取消已发布的作业。")
async def cancel_assignment(assignment_id: int):
    assignment = await Assignment.get_or_none(id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="作业未找到")

    # 假设我们在模型中有一个字段来表示作业是否被取消
    assignment.is_cancelled = True  
    await assignment.save()
    return {"message": "作业已取消"}

@teacher.get("/submissions", summary="获取作业提交结果", description="获取学生的作业提交结果。")
async def get_submissions(assignment_id: int):
    submissions = await Submission.filter(assignment_id=assignment_id)

    # 返回提交的详细信息，包括学生ID和提交信息
    return [{
        "id": submission.id,
        "file_path": submission.file_path,
        "remark": submission.remark,
        "student_id": submission.student_id  # 获取学生ID
    } for submission in submissions]
