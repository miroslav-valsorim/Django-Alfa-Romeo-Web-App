# Azure Deployment Settings

Due to the different structure that my project has and it's 1 folder nested inside, there are few things that have to be set differently from the 'normal' setup

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


## Additional Information.  

If using the alfa_romeo_web folder as root folder (same level as manage.py !!!) use the azure.sh that's different than the azure.sh inside my root folder in this current project !   
Once you check both azure.sh ,the one inside the alfa_romeo_web folder is a bit different, that's because you can use also use those commands directly (python manage.py migrate, etc...) in the SSH in Azure. I'm runing 'python manage.py makemigrations' because there is no migration for the ipn table for PayPal. Pay attention to the DATABASE_URL! You have to 'translate' the AZURE_POSTGRESQL_CONNECTIONSTRING (that will generate in azure enviroments) to a DATABASE_URL. You can find more information on how to do that in google, chatGPT, etc.
CSRF_TRUSTED_ORIGINS is also important, without it the application won't work with any data from you database. Setting up the other env variables, check the screenshot from step 2.

