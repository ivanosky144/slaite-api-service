from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import authRoutes, userRoutes, eventRoutes, notificationRoutes, taskRoutes, activityRoutes, scheduleRoutes
from config.database import Base
from config.database import engine

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(authRoutes.router, prefix="/api/auth")
app.include_router(userRoutes.router, prefix="/api/user")
app.include_router(eventRoutes.router, prefix="/api/event")
app.include_router(activityRoutes.router, prefix="/api/activity")
app.include_router(taskRoutes.router, prefix="/api/task")
app.include_router(notificationRoutes.router, prefix="/api/notification")
app.include_router(scheduleRoutes.router, prefix="/api/schedule")

if __name__ == "__main__": 
    uvicorn.run("main:app", reload=True)