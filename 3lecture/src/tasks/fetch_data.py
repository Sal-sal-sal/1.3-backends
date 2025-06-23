# import requests
# from celery_app import celery_app
# from database import SyncSessionLocal
# from tasks.models import Task
# from datetime import datetime
# import logging

# logger = logging.getLogger(__name__)

# @celery_app.task
# def fetch_and_save_data():
#     """
#     Fetch data from a website and save it to the database.
#     This task is scheduled to run every day.
#     """
#     url = "https://example.com/data"  # Замените на нужный URL
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.text  # Или response.json(), если нужен JSON

#         db = SyncSessionLocal()
#         # Пример: сохраняем как Task (замените на свою модель и логику)
#         new_task = Task(
#             title=f"Fetched data {datetime.utcnow().isoformat()}",
#             description=data[:200],  # Сохраняем первые 200 символов
#             completed=False
#         )
#         db.add(new_task)
#         db.commit()
#         db.refresh(new_task)
#         db.close()
#         logger.info(f"Fetched and saved data from {url}")
#         return {"status": "success", "task_id": new_task.id}
#     except Exception as exc:
#         logger.error(f"Failed to fetch or save data: {exc}")
#         raise exc
