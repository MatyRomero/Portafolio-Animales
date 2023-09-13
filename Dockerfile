FROM ubuntu:22.04
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

ADD ./conf/requirements.txt /code/
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    python3-pip \
    python3-dev \
    libmysqlclient-dev \
    unzip \
    pkg-config

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ./ /code/

ARG DJANGO_APP
ENV DJANGO_APP=${DJANGO_APP}
EXPOSE 8000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 ${DJANGO_APP}.wsgi:application"]


# FROM ubuntu:22.04

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN mkdir /code
# WORKDIR /code

# # Agregar actualización y actualización de paquetes del sistema
# RUN apt-get update && apt-get upgrade -y

# # Instalar paquetes básicos y Python 3
# RUN apt-get -y install build-essential python3-dev python3-pip wget libmysqlclient-dev unzip

# # Actualizar pip y establecer una versión específica
# RUN python3 -m pip install --upgrade pip==21.2.4

# # Instalar el módulo 'cx_Oracle'
# RUN python3 -m pip install cx_Oracle

# # Copiar y instalar dependencias
# COPY ./conf/requirements.txt /code/
# RUN pip install -r requirements.txt

# # Copiar el código fuente
# COPY ./ /code/

# ARG DJANGO_APP
# ENV DJANGO_APP=${DJANGO_APP}
# EXPOSE 8000

# # Cambiar el comando CMD para usar comillas dobles y evitar problemas con expansión de variables
# CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:8000 ${DJANGO_APP}.wsgi:application"]
