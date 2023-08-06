# README #

Este repositorio hospeda una libreria python la cual sera usada desde el repositorio principal.
Esta libreria contiene utilidades para conectarse a una maquina virtual remota, en este caso se trata de una maquina virtual de windows.


### Release

En el caso de que se quiera publicar una nueva version de la libreria, siga las siguientes instrucciones https://packaging.python.org/tutorials/packaging-projects/

Un target ha sido añadido para facilitar este proceso. En el caso de que desee publicar una nueva version, actualice la version del paquete en el archivo `setup.bat`, y ejecute `make publish`.
El paquete puede ser visualizado en la pagina de pypi https://pypi.org/project/ssh-client/