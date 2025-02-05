from src.core.worker import celery_app

@celery_app.task
def notify_external_service(file_name):
    """
    Уведомление внешнего сервиса о появлении нового файла.
    """
    # Отправка уведомления через RabbitMQ
    print(f"Notifying external service about file {file_name}")
    # Здесь можно добавить логику отправки сообщения через RabbitMQ
