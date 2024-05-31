# Real Time Chat
REAL Time Chat Application using Python, Django, Channels, Redis, Websockets

## Features

Authentication and Authorization
- JWT Authentication
- Login
- Signup
- Forgot Password
- Login Change Password
- Reset Password

Chat
- One to One Chat
- Create Group
- Delete Group
- Group Chat
- Message Sent
- Chat History
- Room List 
- Create Room
- Delete Room  

## Automatic Installation
1. Change the permissions for deployment_script.sh

```chmod +x deployment_script.sh```

2. Run deployment_script.sh

```./deployment_script.sh```

3. Create Super User

```python manage.py createsuperuser```

4. create a .env file, refer to .env_example for env variables

5. This script will create database with following credentials, add them to your .env file
- Database Name = test_db
- Database User = test
- Database Password = admin@1234

## Manual Installation



1. Change the working directory

```cd realtime_chat_app/```

2. Create Virtual Environment

``` python3 -m venv venv```

3. Activate Virtual Environment

```source venv/bin/activate```

4. Install dependencies

```pip install -r requirements.txt```

5. Migrate Database

```python manage.py migrate```

6. Create Super User

```python manage.py createsuperuser```

7. Run the server

```python manage.py runserver```

8. Open the browser and go to http://127.0.0.1:8000

9. Login with username: '' and password: '' to access the admin panel at http://127.0.0.1:8000

## Postman Collection
[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/24156324-31834ee5-6cf8-4101-a11c-74bc1bac6c52?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D24156324-31834ee5-6cf8-4101-a11c-74bc1bac6c52%26entityType%3Dcollection%26workspaceId%3D96c0031e-1140-4c22-a1b7-49bed3de958e)
