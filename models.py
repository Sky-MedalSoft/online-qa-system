from tortoise import fields
from tortoise.models import Model

class User(Model):
    """
    用户模型
    """
    id = fields.IntField(pk=True, description="用户ID")
    username = fields.CharField(max_length=20, unique=True, description="用户名")
    password = fields.CharField(max_length=128, description="密码")
    role = fields.CharField(max_length=10, description="角色（student, teacher, principal）")

    class Meta:
        table = "users"
        table_description = "用户表"

class Class(Model):
    """
    班级模型
    """
    id = fields.IntField(pk=True, description="班级ID")
    name = fields.CharField(max_length=50, description="班级名称")
    teacher_id = fields.IntField(description="班主任ID")

    class Meta:
        table = "classes"
        table_description = "班级表"

class Student(Model):
    """
    学生模型
    """
    id = fields.IntField(pk=True, description="学生ID")
    user = fields.OneToOneField('models.User', related_name='profile', on_delete=fields.CASCADE)  # 设定用户关系
    class_id = fields.IntField(description="所属班级ID")

    class Meta:
        table = "students"
        table_description = "学生表"

class Assignment(Model):
    """
    作业模型
    """
    id = fields.IntField(pk=True, description="作业ID")
    title = fields.CharField(max_length=100, description="作业标题")
    content = fields.TextField(description="作业内容")
    start_date = fields.DateField(description="开始日期")
    end_date = fields.DateField(description="截止日期")
    class_id = fields.IntField(description="所属班级ID")

    class Meta:
        table = "assignments"
        table_description = "作业表"

class Submission(Model):
    """
    提交作业模型
    """
    id = fields.IntField(pk=True, description="提交ID")
    assignment_id = fields.IntField(description="作业ID")
    student_id = fields.IntField(description="学生ID")
    file_path = fields.CharField(max_length=255, description="文件路径")
    remark = fields.TextField(description="备注")

    class Meta:
        table = "submissions"
        table_description = "提交作业表"
