from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Student, Assignment, Submission, User

router = APIRouter()


# 定义作业应答模型
class AssignmentResponse(BaseModel):
    id: int
    title: str
    content: str
    start_date: str
    end_date: str


# 定义作业提交请求的模型
class SubmissionRequest(BaseModel):
    assignment_id: int
    file_path: str
    remark: str


@router.get("/my_classes/{user_id}", summary="获取学生班级信息", description="根据用户ID获取学生所在班级的信息。")
async def get_my_classes(user_id: int):
    # 根据 user_id 查找用户
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 查找对应的学生记录
    student = await Student.get_or_none(user_id=user.id)  # 使用 user_id 查找学生
    if not student:
        raise HTTPException(status_code=404, detail="学生未找到")

    return {"class_id": student.class_id}



@router.get("/class_members/{class_id}", summary="获取班级成员", description="获取指定班级的所有学生成员。")
async def get_class_members(class_id: int):
    students = await Student.filter(class_id=class_id)
    return [{"id": student.id, "user_id": student.user_id} for student in students]


@router.get("/assignments/{user_id}", summary="获取作业列表", description="根据用户ID获取学生所在班级的作业列表。")
async def get_assignments(user_id: int):
    # 根据 user_id 查找用户
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 查找对应的学生记录
    student = await Student.get_or_none(user_id=user.id)
    if not student:
        raise HTTPException(status_code=404, detail="学生未找到")

    # 根据班级ID获取作业列表
    assignments = await Assignment.filter(class_id=student.class_id)
    return [
        {
            "id": assignment.id,
            "title": assignment.title,
            "content": assignment.content,
            "start_date": assignment.start_date,
            "end_date": assignment.end_date,
        } for assignment in assignments
    ]


@router.get("/assignment/{assignment_id}", summary="获取作业详情", description="根据作业ID获取作业的详细信息。")
async def get_assignment_details(assignment_id: int):
    assignment = await Assignment.get_or_none(id=assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="作业未找到")

    return {
        "id": assignment.id,
        "title": assignment.title,
        "content": assignment.content,
        "start_date": assignment.start_date,
        "end_date": assignment.end_date,
    }


@router.post("/submit_assignment", summary="提交作业", description="提交作业，确保不可重复提交。")
async def submit_assignment(submission: SubmissionRequest, user_id: int):
    # 根据 user_id 查找用户
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 根据 user_id 查找学生记录
    student = await Student.get_or_none(user_id=user.id)
    if not student:
        raise HTTPException(status_code=404, detail="学生未找到")

    # 根据作业 ID 查找作业
    assignment = await Assignment.get_or_none(id=submission.assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="作业未找到")

    # 检查是否已提交作业
    existing_submission = await Submission.get_or_none(
        assignment_id=submission.assignment_id,
        student_id=student.id  # 使用学生ID
    )
    if existing_submission:
        raise HTTPException(status_code=400, detail="作业已提交不可重复提交")

    # 创建并保存作业提交
    new_submission = Submission(
        assignment_id=submission.assignment_id,
        student_id=student.id,  # 使用学生ID
        file_path=submission.file_path,
        remark=submission.remark
    )
    await new_submission.save()

    return {"message": "作业提交成功"}
