from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from models import User, Student

# 初始化密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reg = APIRouter()
manager = APIRouter()

# 定义用户注册模型
class UserRegister(BaseModel):
    username: str
    password: str
    role: str  # 角色：'student', 'teacher', 'principal'
    class_id: int  # 添加班级ID

@reg.post("/register", description="用户注册", summary="注册新用户")
async def register(user: UserRegister):
    """
    用户注册接口。
    根据提供的用户名、密码和角色，在系统中创建新的用户账户。
    如果角色为学生，同时在学生表中添加记录。
    """
    # 检查用户名是否已存在
    existing_user = await User.get_or_none(username=user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 哈希处理密码
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed_password, role=user.role)

    # 保存新用户
    await new_user.save()
    # 如果角色是学生，自动在学生表中增加数据
    if user.role == "student":
        new_student = Student(user_id=new_user.id, class_id=user.class_id)
        await new_student.save()

    return {
        "message": "用户注册成功",
        "username": new_user.username,
        "role": new_user.role
    }

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

class PasswordChange(BaseModel):
    username: str
    old_password: str
    new_password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@manager.post("/login", response_model=UserResponse, description="用户登录", summary="用户登录接口")
async def login(user: UserLogin):
    """
    用户登录接口。
    输入用户名和密码以进行身份验证，成功后返回用户的基本信息。
    """
    db_user = await User.get_or_none(username=user.username)
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    return {
        "id": db_user.id,
        "username": db_user.username,
        "role": db_user.role,
    }

@manager.get("/user_info/{user_id}", response_model=UserResponse, description="获取用户信息", summary="获取用户信息接口")
async def get_user_info(user_id: int):
    """
    获取用户信息接口。
    根据用户ID获取用户的详细信息。
    """
    db_user = await User.get_or_none(id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="用户未找到")

    return {
        "id": db_user.id,
        "username": db_user.username,
        "role": db_user.role,
    }

@manager.put("/change_password", description="修改密码", summary="修改用户密码接口")
async def change_password(password_change: PasswordChange):
    """
    修改密码接口。
    用户提供用户名、旧密码和新密码，进行密码更改操作。
    """
    db_user = await User.get_or_none(username=password_change.username)

    if db_user is None or not verify_password(password_change.old_password, db_user.password):
        raise HTTPException(status_code=400, detail="旧密码错误或用户未找到")

    hashed_new_password = pwd_context.hash(password_change.new_password)
    db_user.password = hashed_new_password
    await db_user.save()

    # 返回用户的基本信息和成功消息
    return {
        "message": "密码修改成功",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "role": db_user.role,
        }
    }
