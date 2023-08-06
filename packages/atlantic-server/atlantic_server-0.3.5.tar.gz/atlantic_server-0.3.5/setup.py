# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atlantic_server',
 'atlantic_server.atl',
 'atlantic_server.com',
 'atlantic_server.smd']

package_data = \
{'': ['*'], 'atlantic_server.smd': ['documents/*']}

install_requires = \
['Django>=2.2,<3.0',
 'cffi>=1.14.0,<2.0.0',
 'django-filter>=2,<3',
 'djangorestframework>=3,<4',
 'drf-nested-routers>=0.91,<0.92',
 'lxml>=4,<5',
 'mysqlclient>=2,<3',
 'pygit2>=1.2,<1.3',
 'wheel>=0.35.1,<0.36.0']

entry_points = \
{'console_scripts': ['atlantic_server = atlantic_server.manage:main']}

setup_kwargs = {
    'name': 'atlantic-server',
    'version': '0.3.5',
    'description': 'Server side of an application of an Aircraft Technical Log',
    'long_description': '# Atlantic \n\nThis program is the sever side of the Atlantic app. It gives you a restful api.\n\n## Installation on debian 10 (or ubuntu 20.04) for production\n\nThe recommended way to install it is to use a virtual environment.\n\n1. Install package\n    ```\n    apt install -y pipx apache2 libapache2-mod-wsgi-py3 mariadb-server python3-dev libmariadb-dev libmariadbclient-dev build-essential\n    ```\n\n2. Create and configure database\n    ```\n    mysql -u root -p\n    CREATE DATABASE atlantic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;\n    CREATE USER \'aristide\'@\'localhost\' IDENTIFIED BY \'password\';\n    GRANT ALL PRIVILEGES ON atlantic . * TO \'aristide\'@\'localhost\';\n    FLUSH PRIVILEGES;\n    quit;\n    ```\n\n3. Create a user and log it\n    ```\n    adduser aristide\n    su - aristide\n    ```\n\n4. Install atlantic_server\n    ```\n    pipx install atlantic_server\n    ```\n\n5. In the user home directory, create a conf.py file\n    ```\n    nano ~/conf.py\n    ```\n    and paste following parameters (with adjust):\n    ```\n    SECRET_KEY = "enter here a lot of randoms letters and numbers here"\n    DEBUG = True\n    DATABASES = {\n        "default": {\n            "ENGINE": "django.db.backends.mysql",\n            "NAME": "aristide",\n            "USER": "atlantic",\n            "PASSWORD": "password",\n        }\n    }\n    MEDIA_ROOT = "/home/aristide/www/media/"\n\n6. Configure Django app\n    ```\n    atlantic_server makemigrations com atl smd \n    atlantic_server migrate\n    atlantic_server collectstatic\n    atlantic_server createsuperuser\n    ```\n\n7. Configure Apache2\n    - Return to root user\n        ```\n        exit\n        ```\n    - Create a new file\n        ```\n        nano /etc/apache2/site-available/atlantic.conf\n        ```\n    - Paste following parameters (with adjust):\n        ```\n        <VirtualHost *:80>\n            ServerName url.for.your.site\n            ErrorLog ${APACHE_LOG_DIR}/error.log\n            CustomLog ${APACHE_LOG_DIR}/access.log combined\n            DocumentRoot /home/aristide/www/vue/\n            <Directory /home/aristide/.local/pipx/venvs/atlantic-server/lib/python3.7/site-packages/atlantic_server>\n                <Files wsgi.py>\n                    Require all granted\n                </Files>\n            </Directory>\n            WSGIPassAuthorization On\n            WSGIDaemonProcess aristide python-home=/home/aristide/.local/pipx/venvs/atlantic-server python-path=/home/aristide\n            WSGIProcessGroup aristide\n            WSGIScriptAlias /admin /home/aristide/.local/pipx/venvs/atlantic-server/lib/python3.7/site-packages/atlantic_server/wsgi.py/admin\n            WSGIScriptAlias /api /home/aristide/.local/pipx/venvs/atlantic-server/lib/python3.7/site-packages/atlantic_server/wsgi.py/api\n            <Directory /home/aristide/www/>\n                    Require all granted\n            </Directory>\n            Alias /media/ /home/aristide/www/media/\n            Alias /static/ /home/aristide/www/static/\n        </VirtualHost>\n        ```\n    The DocumentRoot directory is the place where you upload the atlantic_client side.\n\n    - Save and close file\n\n\n8. Enabled site for apache\n    ```\n    a2dissite *\n    a2ensite atlantic\n    systemctl reload apache2\n    ```\n\n9. It is recommended to secure the access of your site with a certificate...',
    'author': 'Matthieu Nué',
    'author_email': 'matthieu.nue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
