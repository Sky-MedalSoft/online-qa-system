from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `students` MODIFY COLUMN `user_id` INT NOT NULL;
        ALTER TABLE `students` ADD UNIQUE INDEX `uid_students_user_id_ccd731` (`user_id`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `students` DROP INDEX `idx_students_user_id_ccd731`;
        ALTER TABLE `students` MODIFY COLUMN `user_id` INT NOT NULL  COMMENT '用户ID';"""
