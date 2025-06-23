from asyncio import wait
from fastapi import APIRouter, Depends, Body, Path, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_async_db
from tasks.models import TaskCreate, TaskUpdate, Task as TaskResponse
from tasks.crud import TaskCRUD
from celery_tasks import send_notification_task
from tasks.models import TaskCreateDelay    
from tasks.crud import delay
router = APIRouter()

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate = Body(...),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new task"""
    # Сохраняем созданную задачу в переменную
    new_task = await TaskCRUD.create_task(db, task)
    # Возвращаем ее
    return new_task


@router.post("/tasks/delay", response_model=TaskResponse)
async def create_task_with_celery_delay(
    task: TaskCreateDelay = Body(...),
    db: AsyncSession = Depends(get_async_db)
):
    """Create a new task with Celery delay (использует apply_async)"""
    # Отправляем задачу на отправку уведомления с задержкой через Celery
    send_notification_task.apply_async(
        args=[task.description, task.recipient],
        countdown=task.delay_seconds
    )
    # Сохраняем задачу сразу (без задержки)
    new_task = await TaskCRUD.create_task(db, task)
    return new_task



@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int = Path(..., description="The ID of the task to retrieve"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific task by ID"""
    return await TaskCRUD.get_task(db, task_id)

@router.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of tasks to return"),
    db: AsyncSession = Depends(get_async_db)
):
    """Get all tasks with pagination"""
    return await TaskCRUD.get_tasks(db, skip=skip, limit=limit)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int = Path(..., description="The ID of the task to update"),
    task: TaskUpdate = Body(...),
    db: AsyncSession = Depends(get_async_db)
):
    """Update a specific task"""
    return await TaskCRUD.update_task(db, task_id, task)

@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int = Path(..., description="The ID of the task to delete"),
    db: AsyncSession = Depends(get_async_db)
):  
    """Delete a specific task"""
    return await TaskCRUD.delete_task(db, task_id)

@router.post("/send_notification")
async def send_notification_with_delay(
    message: str = Body(...),
    recipient: str = Body(...),
    delay_seconds: int = Body(10, embed=True)
):
    """
    Send notification with a delay using Celery
    """
    from celery_tasks import send_notification
    result = send_notification.apply_async(args=[message, recipient], countdown=delay_seconds)
    return {"task_id": result.id, "status": "queued", "delay": delay_seconds}

@router.post("/wait_and_send_notification")
async def wait_and_send_notification(
    message: str = Body(...),
    recipient: str = Body(...),
    wait_seconds: int = Body(10, embed=True)
):
    """
    Wait n seconds before sending notification (blocking, for demo only!)
    """
    import asyncio
    await asyncio.sleep(wait_seconds)
    result = send_notification_task.apply_async(args=[message, recipient])
    return {
        "task_id": result.id,
        "status": "queued after wait",
        "waited": wait_seconds
    }

@router.post("/tasks/remind", response_model=TaskResponse)
async def create_task_with_reminder(
    task: TaskCreateDelay = Body(...),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Create a new task and отправить напоминание через N часов (использует Celery apply_async)
    """
    # Сохраняем задачу сразу
    new_task = await TaskCRUD.create_task(db, task)
    # Считаем задержку в секундах
    delay_seconds = task.delay_seconds if hasattr(task, 'delay_seconds') else 0
    # Отправляем напоминание через Celery с задержкой
    send_notification_task.apply_async(
        args=[f"Напоминание о задаче: {task.title}", task.recipient],
        countdown=delay_seconds
    )
    return new_task
