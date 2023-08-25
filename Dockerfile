FROM ubuntu:22.04

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN export PATH="$PATH:~/.yarn/bin"

RUN mkdir /code
WORKDIR /code

# Agregar actualización y actualización de paquetes del sistema
RUN apt-get update && apt-get upgrade -y

# Instalar paquetes básicos y Python 3
RUN apt-get -y install build-essential python3-dev python3-pip wget libmysqlclient-dev unzip

# Actualizar pip y establecer una versión específica
RUN python3 -m pip install --upgrade pip==21.2.4

# Copiar y instalar dependencias
ADD ./conf/requirements.txt /code/
RUN pip install -r requirements.txt

# Copiar el código fuente
ADD ./ /code/

ARG DJANGO_APP
ENV DJANGO_APP=${DJANGO_APP}
EXPOSE 8000

# Cambiar el comando CMD para usar comillas dobles y evitar problemas con expansión de variables
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 ${DJANGO_APP}.wsgi:application"]
