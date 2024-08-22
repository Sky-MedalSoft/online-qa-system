from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.general import pwd_context
from models import User, Student, Class

admin = APIRouter()


# 定义用户创建、更新模型
class TeacherCreate(BaseModel):
    username: str
    password: str


class TeacherUpdate(BaseModel):
    id: int
    username: str
    password: str


# 定义学生创建模型
class StudentCreate(BaseModel):
    username: str
    password: str
    class_id: int  # 班级ID


class StudentUpdate(BaseModel):
    username: str


# 创建教师
@admin.post("/teachers", summary="创建教师", description="创建新的教师账户。")
async def create_teacher(teacher_data: TeacherCreate):
    existing_teacher = await User.get_or_none(username=teacher_data.username)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="教师已存在")

    new_teacher = User(username=teacher_data.username, password=teacher_data.password, role="teacher")
    await new_teacher.save()

    return {"message": "教师创建成功"}


# 获取所有教师
@admin.get("/teachers", summary="获取教师列表", description="获取所有教师的列表。")
async def get_teachers():
    teachers = await User.filter(role="teacher")
    return [{"id": teacher.id, "username": teacher.username} for teacher in teachers]


# 更新教师
@admin.put("/teachers", summary="更新教师信息", description="更新现有教师的账户信息。")
async def update_teacher(teacher_update: TeacherUpdate):
    teacher = await User.get_or_none(id=teacher_update.id)
    if not teacher:
        raise HTTPException(status_code=404, detail="教师未找到")

    teacher.username = teacher_update.username
    teacher.password = teacher_update.password  # 这里可以加密处理
    await teacher.save()

    return {"message": "教师信息更新成功"}


# 删除教师
@admin.delete("/teachers/{teacher_id}", summary="删除教师", description="根据教师ID删除教师账户。")
async def delete_teacher(teacher_id: int):
    teacher = await User.get_or_none(id=teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="教师未找到")

    await teacher.delete()  # 删除教师记录
    return {"message": "教师删除成功"}


# 创建学生
@admin.post("/students", summary="创建学生", description="创建新的学生账户，并在students表中同步更新。")
async def create_student(student_data: StudentCreate):
    # 检查用户名是否已存在
    existing_student = await User.get_or_none(username=student_data.username)
    if existing_student:
        raise HTTPException(status_code=400, detail="学生已存在")

    # 创建新用户
    hashed_password = pwd_context.hash(student_data.password)
    new_user = User(username=student_data.username, password=hashed_password, role="student")
    await new_user.save()

    # 同步更新students表
    new_student_record = Student(user_id=new_user.id, class_id=student_data.class_id)

    if student_data.class_id is None:
        raise HTTPException(status_code=400, detail="班级ID不能为NULL")

    await new_student_record.save()

    return {"message": "学生创建成功"}


# 获取所有学生
@admin.get("/students", summary="获取学生列表", description="获取所有学生的列表。")
async def get_students():
    students = await Student.all()
    return [{"id": student.id, "username": student.user.username} for student in students]


@admin.put("/students/{user_id}", summary="更新学生信息", description="更新现有学生的账户信息。")
async def update_student(user_id: int, student_update: StudentUpdate):
    # 查找根据用户ID获取用户对象
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新用户的用户名
    user.username = student_update.username  # 只更新用户名
    await user.save()  # 保存用户信息

    return {"message": "学生信息更新成功"}

@admin.delete("/students/{user_id}", summary="删除学生", description="根据用户ID删除学生账户。")
async def delete_student(user_id: int):
    # 查找用户对象
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 查找学生对象
    student = await Student.get_or_none(user_id=user.id)
    if student:
        await student.delete()  # 删除学生记录

    await user.delete()  # 删除用户
    return {"message": "学生和相关账户删除"}