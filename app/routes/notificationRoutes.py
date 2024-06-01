from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from models.userModel import User
from models.notificationModel import Notification
from models.activityModel import Activity
from datetime import datetime
from dto.notificationObjects import NotificationBody
from config.database import get_db
import asyncio
from middleware.authentication import verifyAuth

router = APIRouter(tags=["Notifications"])

@router.websocket("/{user_id}", dependencies=[Depends(verifyAuth)])
async def pushNotifications(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()

    try:
        while True:
            current_time = datetime.now()
            notifications = db.query(Notification).filter(Notification.user_id == user_id, Notification.time == current_time).all()

            for notification in notifications:
                payload = {
                    "message": notification.message,
                    "status": notification.status,
                    "time": notification.times
                }
                await websocket.send_json(payload)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass

@router.post("/", dependencies=[Depends(verifyAuth)])
def createNotification(notification: NotificationBody, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == notification.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_notification = Notification(
        message = notification.message,
        status = notification.status,
        time = notification.time,
        user_id = notification.user_id,
        activity_id = notification.activity_id
    )
    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return {
        "status": "success",
        "message": "New notification has been created"
    }

@router.put("/{notification_id}", dependencies=[Depends(verifyAuth)])
def updateNotification(notification_id: int, notification: NotificationBody, db: Session = Depends(get_db)):
    existing_notification = db.query(Notification).filter(Notification.id == notification_id).first()

    if not existing_notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    existing_notification.status = notification.status
    existing_notification.time = notification.time
    existing_notification.updated_at = datetime.now()

    db.commit()

@router.get("/{activity_id}", dependencies=[Depends(verifyAuth)])
def getNotificationsByActivity(activity_id: int, db: Session = Depends(get_db)):
    existing_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not existing_activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    list_notifications = db.query(Notification).filter(Notification.activity_id == activity_id)

    return {
        "status": "success",
        "data": list_notifications
    }

