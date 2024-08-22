from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import User, Class, Student, Assignment, Submission

teacher = APIRouter()


class ClassCreate(BaseModel):
    name: str
    teacher_id: int  # 教师ID


class ClassUpdate(BaseModel):
    id: int
    name: str


class StudentCreate(BaseModel):
    username: str
    password: str
    class_id: int


class StudentUpdate(BaseModel):
    id: int
    username: str


class AssignmentCreate(BaseModel):
    title: str
    content: str
    start_date: str  # YYYY-MM-DD
    end_date: str
    class_id: int


@teacher.get("/classes")
async def get_classes(teacher_id: int):
    classes = await Class.filter(teacher_id=teacher_id)
    return classes


@teacher.get("/students")
async def get_students(class_id: int):
    students = await Student.filter(class_id=class_id).prefetch_related('user')
    return [student.user for student in students]



@teacher.post("/class")
async def create_class(class_data: ClassCreate):
    new_class = Class(name=class_data.name, teacher_id=class_data.teacher_id)
    await new_class.save()
    return {"message": "班级创建成功"}


@teacher.put("/class")
async def update_class(class_update: ClassUpdate):
    class_to_update = await Class.get_or_none(id=class_update.id)
    if not class_to_update:
        raise HTTPException(status_code=404, detail="班级未找到")

    class_to_update.name = class_update.name
    await class_to_update.save()
    return {"message": "班级更新成功"}


@teacher.delete("/class/{class_id}")
async def delete_class(class_id: int):
    class_to_delete = await Class.get_or_none(id=class_id)
    if not class_to_delete:
        raise HTTPException(status_code=404, detail="班级未找到")

    await class_to_delete.delete()
    return {"message": "班级删除成功"}


@teacher.post("/student")
async def create_student(student_data: StudentCreate):
    existing_student = await User.get_or_none(username=student_data.username)
    if existing_student:
        raise HTTPException(status_code=400, detail="学生已存在")

    new_user = User(username=student_data.username, password=student_data.password, role="student")
    await new_user.save()

    new_student = Student(user=new_user, class_id=student_data.class_id)
    await new_student.save()

    return {"message": "学生创建成功"}


@teacher.put("/student")
async def update_student(student_update: StudentUpdate):
    student = await Student.get_or_none(id=student_update.id)
    if not student or student.user.role != "student":
        raise HTTPException(status_code=404, detail="学生未找到或角色错误")

    student.user.username = student_update.username
    await student.user.save()

    return {"message": "学生信息更新成功"}


@teacher.delete("/student/{student_id}")
async def delete_student(student_id: int):
    student = await Student.get_or_none(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生未找到")

    await student.user.delete()  # 删除用户信息和相关学生
    return {"message": "学生删除成功"}


@teacher.post("/assignment")
async def create_assignment(assignment_data: AssignmentCreate):
    new_assignment = Assignment(
        title=assignment_data.title,
        content=assignment_data.content,
        start_date=assignment_data.start_date,
        end_date=assignment_data.end_date,
        class_id=assignment_data.class_id
    )
    await new_assignment.save()
    return {"message": "作业已发布"}


@teacher.get("/assignments")
async def get_assignments(class_id: int):
    assignments = await Assignment.filter(class_id=class_id)
    return assignments


@teacher.put("/assignment/{assignment_id}/cancel")
async def cancel_assignment(assignment_id: int):
    assignment = await Assignment.get_or_none(id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="作业未找到")

    assignment.is_cancelled = True  # 假设我们在模型中有这个字段来表示作业是否被取消
    await assignment.save()

    return {"message": "作业已取消"}


@teacher.get("/submissions")
async def get_submissions(assignment_id: int):
    submissions = await Submission.filter(assignment_id=assignment_id).prefetch_related('student')
    return submissions
