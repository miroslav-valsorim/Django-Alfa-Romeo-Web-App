Version 1.1 of running my application in single Kubernetes cluster, all files and steps provided. Still a lot of things to clear out. Everything with the website works as expected, some features are not working due to the fact few env miss like smtp mail and etc. (while registering will throw error 500, but you will still be registered.)

Difference from Version1:
- Now there is no need to run the migrate and collectstatic commands in the container, there is 'initCOntainer' that does this for us. Also create superuser can be added if needed and few other steps !
- Deployment and Service manifests are now split for both DB and WEB.
- Added 'faster' way to execute all comands at once

For this setup you need:
- Oracle VirtualBox
- Minikube
- kubectl
