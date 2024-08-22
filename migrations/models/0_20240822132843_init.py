from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `assignments` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '作业ID',
    `title` VARCHAR(100) NOT NULL  COMMENT '作业标题',
    `content` LONGTEXT NOT NULL  COMMENT '作业内容',
    `start_date` DATE NOT NULL  COMMENT '开始日期',
    `end_date` DATE NOT NULL  COMMENT '截止日期',
    `class_id` INT NOT NULL  COMMENT '所属班级ID'
) CHARACTER SET utf8mb4 COMMENT='作业表';
CREATE TABLE IF NOT EXISTS `classes` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '班级ID',
    `name` VARCHAR(50) NOT NULL  COMMENT '班级名称',
    `teacher_id` INT NOT NULL  COMMENT '班主任ID'
) CHARACTER SET utf8mb4 COMMENT='班级表';
CREATE TABLE IF NOT EXISTS `students` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '学生ID',
    `user_id` INT NOT NULL  COMMENT '用户ID',
    `class_id` INT NOT NULL  COMMENT '所属班级ID'
) CHARACTER SET utf8mb4 COMMENT='学生表';
CREATE TABLE IF NOT EXISTS `submissions` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '提交ID',
    `assignment_id` INT NOT NULL  COMMENT '作业ID',
    `student_id` INT NOT NULL  COMMENT '学生ID',
    `file_path` VARCHAR(255) NOT NULL  COMMENT '文件路径',
    `remark` LONGTEXT NOT NULL  COMMENT '备注'
) CHARACTER SET utf8mb4 COMMENT='提交作业表';
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(20) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL  COMMENT '密码',
    `role` VARCHAR(10) NOT NULL  COMMENT '角色（student, teacher, principal）'
) CHARACTER SET utf8mb4 COMMENT='用户表';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
