"""启动脚本"""
#uvicorn：第三方库，是一个ASGI服务器，负责真正把网站跑起来，接受浏览器请求的那个服务器引擎
import uvicorn
from app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "app.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )

