# Azure Deployment Settings

Due to the different structure that my project has and it's 1 folder nested inside, there have to be set differently from the 'normal' setup

## Steps and comments

1. Select WebApp + Database:  

    - ![FirstPage](screenshots/1.png)   

    - ![SecondPage](screenshots/2.png)    

    - After Project is done it has to look like this   

    - ![ThirdPage](screenshots/3.png)   

2. Set Environment Variables:   

    - ![FourthPage](screenshots/4.png)   

3. Set Start Command:   

    - Check azure.sh inside the project that's in the root project

    - ![FifthPage](screenshots/5.png)   

4. Deploy the project from GitHub   

    - ![SixthPage](screenshots/6.png)   

5. Go to SSH and create Superuser (log inside the vm)   

    - ![SeventhPage](screenshots/7.png)   

    - first use ```cd alfa_romeo_web```

    - ![EightPage](screenshots/8.png)

    - ```python manage.py createsuperuser```

6. Open Web Page

    - ![NinethPage](screenshots/9.png)