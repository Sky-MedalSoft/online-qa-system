请使用 FastAPI 框架、Python3.10、MySQL（或 Sqlite）、Redis（可选） 完成以下的项目需求：

* 建立在线git仓库（可选：公司 gitlab、gitee、GitHub），邀请我作为查阅者（即 具有访问权限）
* 在线师生问答系统，需求文档在下方
* 功能开发过程中，需要编写接口文档，推荐使用 Apifox

产品分为三个端：
老师端：可以进行学生管理、班级管理、作业发布
学生端：可以查看自己所在班级、同学、作业提交
校长端（超级管理员）：可以对老师进行CRUD、可以对学生进行CRUD

产品逻辑如下：
校长登录系统后，可以创建老师，并分配密码；校长拥有所有班级、老师、学生的管理能力；
老师登录系统，创建班级，创建学生并分配密码，可以将学生加入自己创建的班级；选择班级，发布作业，包含作业标题、作业内容、开始日期，截止日期；
学生登录系统，可以看见自己所属的班级以及当前周期内的作业列表；打开班级人员列表，可以看到对应的老师与同学；点击作业，可以上传文件与在输入框内输入备注来提交作业；

预计完成接口如下：
通用：

* 登录接口
* 获取用户信息接口
* 修改密码接口

老师：

* 班级列表接口
* 学生列表接口
* 班级编辑接口（新增、修改、删除）
* 学生编辑接口（新增、编辑（仅可编辑自己创建的）、删除（仅可删除自己创建的））
* 班级成员管理
* 已发布作业列表接口
* 作业提交结果列表接口
* 作业编辑接口（新增、编辑、取消（不是删除））

学生：

* 所在班级列表接口
* 班级成员接口（仅可查看自己所在班级的成员）
* 周期内作业列表接口
* 作业详情接口
* 作业提交接口（不可重复提交）

额外需求（视能力决定要不要继续开发）：

* 运行查看在线的同学与老师，并进行实时聊天
* 首页有智能助手，可进行聊天，智能助手流式响应，即逐字反馈（对接大语言模型）
* 使用Dockerfile进行打包与部署
* 开发对应的前端

已完成内容：

* 接口开发
* 接口文档编写
  地址：https://apifox.com/apidoc/shared-51c1ceb1-cb5c-463b-8922-e9c106aef720
* 首页智能助手（采用流式响应）
* 前端开发（部分）-- index login register 三个页面

未完成内容：

* 前端开发
* 使用Dockerfile进行打包与部署
* 运行查看在线的同学与老师，并进行实时聊天