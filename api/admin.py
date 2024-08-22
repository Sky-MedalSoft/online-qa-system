from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import User, Class

admin = APIRouter()


class TeacherCreate(BaseModel):
    username: str
    password: str


class ClassCreate(BaseModel):
    name: str
    teacher_id: int


@admin.post("/create_teacher")
async def create_teacher(teacher: TeacherCreate):
    existing_teacher = await User.get_or_none(username=teacher.username)
    if existing_teacher:
        raise HTTPException(status_code=400, detail="教师已存在")

    new_teacher = User(username=teacher.username, password=teacher.password, role="teacher")
    await new_teacher.save()
    return {"message": "教师创建成功"}


@admin.post("/create_class")
async def create_class(class_data: ClassCreate):
    teacher = await User.get_or_none(id=class_data.teacher_id)
    if not teacher or teacher.role != "teacher":
        raise HTTPException(status_code=400, detail="无效的教师ID")

    new_class = Class(name=class_data.name, teacher=teacher)
    await new_class.save()
    return {"message": "班级创建成功"}
