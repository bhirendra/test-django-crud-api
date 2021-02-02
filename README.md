# test-django-crud-api


A test project to perform basic CRUD operations.

Follow the below guidelines to run this project for demo.

1. Clone the project using the following command and go to the root directory of the project
    ```
    git clone https://github.com/bhirendra/test-django-crud-api.git
    ```
2. Create super user for django administration using command
    ```
    ./manage.py createsuperuser
    ```
    It will ask for username and password.
3. Now start the django server.
    ```
    ./manage.py runserver 
    ```
4. Go to the django administration page using the following link
    http://localhost:8000/admin/
5. To run the test cases of API's, enter the following command
    ```
    ./manage.py test 
    ```
    
## API Documentation
Open the link http://localhost:8000/doc/

or with neat and clean UI go to http://localhost:8000/doc/redoc/


Good luck and cheers ! :)
