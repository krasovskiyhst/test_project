from datetime import datetime
from .models import AccessLogs
from django.conf import settings
from .celery import app


@app.task()
def parsing_logs():
    def log_line_parsing(line):
        """ Разбор строки """
        split_line = line.split()
        print(split_line)
        return {'ip': split_line[0],
                'date': datetime.strptime(split_line[3].replace('[', '') + split_line[4].replace(']', ''),
                                          '%d/%b/%Y:%H:%M:%S%z'),
                'request_method': split_line[5].replace('"', ''),
                'code_status': int(split_line[8]),
                'data_transfer': int(split_line[9]),
                }

    def writing_data_to_the_database(lines):
        """ Запись строк в БД """
        for line in lines:
            line_dict = log_line_parsing(line)

            AccessLogs.objects.get_or_create(
                ip=line_dict['ip'],
                date=line_dict['date'],
                request_method=line_dict['request_method'],
                code_status=line_dict['code_status'],
                data_transfer=line_dict['data_transfer'],
            )

    try:
        with open(settings.ACCESS_FILE_PATH) as fd:
            lines = fd.readlines()
            writing_data_to_the_database(lines)
    except IOError:
        print("access_log file not found")
