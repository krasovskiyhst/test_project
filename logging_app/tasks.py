from test_project.celery import app


@app.task()
def parsing_logs():
    return
