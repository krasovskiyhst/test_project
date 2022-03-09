Тестовый деплой проекта Django "test_project" на сервер Debian11, с использованием Apache. Настройка Celery + Redis для выполнения периодических задач.
===========
Не забудьте заменить имя "sergey", пароль БД и IP адрес. И сгенерируйте свой SECRET_KEY.

Создание пользователя
-----------
adduser sergey

usermod -aG sudo sergey

groups sergey

Обновить систему
-----------
apt update

apt list --upgradable

apt upgrade

apt install sudo

su sergey	#Переходим на нового юзера

cd

sudo apt install apache2 git libapache2-mod-wsgi-py3 supervisor

Создание базы данных
-----------
sudo apt install postgresql

sudo -u postgres psql

CREATE DATABASE sergey;

CREATE USER sergey WITH PASSWORD '**ВАШ ПАРОЛЬ**';

ALTER ROLE sergey SET client_encoding TO 'utf8';

ALTER ROLE sergey SET default_transaction_isolation TO 'read committed';

ALTER ROLE sergey SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE sergey TO sergey;

\q


Виртуальная среда
-----------
sudo apt-get install python3-venv

python3 -m venv venv

source venv/bin/activate

git clone https://github.com/krasovskiyhst/test_project.git

pip install -U pip

pip install -r test_project/requirements.txt


Создаём файл настроек на сервере
-----------
cd test_project
cat > test_project/production_settings.py

*Содержимое файла:*
``` Python
import os

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'СГЕНЕРИРОВАТЬ КЛЮЧ' # <<<< СГЕНЕРИРОВАТЬ КЛЮЧ

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'IP СЕРВЕРА'] # <<<< ИЗМЕНИТЬ IP СЕРВЕРА

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sergey',
        'USER': 'sergey',
        'PASSWORD': '**ВАШ ПАРОЛЬ**',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

Финальная настройка Django в виртуальном окружении
-----------
python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

python manage.py createsuperuser # Если нужно

deactivate

sudo mkdir /logs


УСТАНОВКА И НАСТРОЙКА REDIS
-----------
sudo apt-get install -y make build-essential tcl #Пакеты для компиляции REDIS

wget http://download.redis.io/redis-stable.tar.gz

tar xvzf redis-stable.tar.gz

rm redis-stable.tar.gz

cd redis-stable

make

sudo make install

Автозапуск Redis
-----------
sudo cp src/redis-server /usr/local/bin/

sudo cp src/redis-cli /usr/local/bin/

sudo mkdir /etc/redis

sudo mkdir /var/redis

sudo cp utils/redis_init_script /etc/init.d/redis_6379


sudo cp redis.conf /etc/redis/6379.conf

sudo mkdir /var/redis/6379

sudo nano /etc/redis/6379.conf

*Изменить в файле:*

```
daemonize установить yes
logfile установить /var/log/redis_6379.log
dir установить /var/redis/6379
```

*ctrl+o, Enter, ctrl+x* #Сохранить и закрыть Nano

sudo update-rc.d redis_6379 defaults

redis-cli	#Чтобы проверить работу редис

ping	#Чтобы проверить работу редис


НАСТРОЙКА APACHE
-----------
cd /etc/apache2/sites-available/

*Добавим файл*

sudo echo > mysite.conf

*Содержимое файла:*
```
<VirtualHost *:80>
	ServerName IP СЕРВЕРА ИЛИ ДОМЕН
	ServerAlias IP СЕРВЕРА ИЛИ ДОМЕН
	DocumentRoot /home/sergey/test_project
	ErrorLog /home/sergey/test_project/logs/error_log
	CustomLog /home/sergey/test_project/logs/access_log common
	Alias /static /home/sergey/test_project/static
	<Directory /home/sergey/test_project/static>
		Require all granted
	</Directory>
	Alias /static /home/sergey/test_project/media
	<Directory /home/sergey/test_project/media>
		Require all granted
	</Directory>
	<Directory /home/sergey/test_project/test_project>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>
	WSGIDaemonProcess test_project python-path=/home/sergey/test_project python-home=/home/sergey/venv
	WSGIProcessGroup test_project
	WSGIScriptAlias / /home/sergey/test_project/test_project/wsgi.py
</VirtualHost>
```

sudo a2ensite mysite.conf

sudo service apache2 restart


Настройка supervisor
-----------
cd /etc/supervisor/conf.d/

sudo ln /home/sergey/test_project/logging_app/config/projectcelery.conf

sudo ln /home/sergey/test_project/logging_app/config/projectcelerybeat.conf

sudo update-rc.d supervisor enable

sudo service supervisor start

sudo supervisorctl reread

sudo supervisorctl update

sudo reboot
