import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from tortoise.contrib.fastapi import register_tortoise
from api.general import reg, manager
from api.admin import admin
from api.teacher import teacher
from api.student import router


from settings import TORTOISE_ORM

app = FastAPI()
templates = Jinja2Templates(directory="templates")

register_tortoise(
    app=app,
    config=TORTOISE_ORM
)

@app.get("/reg", tags=["注册（返回前端页面）"], response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/login", tags=["登录（返回前端页面）"], response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
app.include_router(reg, tags=["注册"])

app.include_router(manager, tags=["信息管理"])

app.include_router(admin, tags=["管理员（校长）"])

app.include_router(teacher, tags=["教师"])

app.include_router(router, tags=["学生"])








if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,log_level="info", reload=True)
