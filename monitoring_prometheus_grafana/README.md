# Monitoring Via Prometheus and Grafana

## Steps to go through

1. Download Prometheus  

2. In the project run ```pip install django-prometheus```  

3. Add it to INSTALLED_APPS  

![Apps](screenshots/apps.png)

4. Add it to the MIDDLEWARE  

![Middleware](screenshots/middleware.png.png)

5. Add it to the main project urlpatterns  

![Urls](screenshots/urls.png)

6. Create the yml file to run your prometheus with the config ```prometheus.exe --config.file=prometheus-alfa-web-app.yml```  

![File](screenshots/file.png)

## Result

![FirstPage](screenshots/1.png)   

![SecondPage](screenshots/2.png)     
    
![ThirdPage](screenshots/3.png)   
  

