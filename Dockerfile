FROM python:3.11-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG="en_US.UTF-8"
ENV LC_ALL="en_US.UTF-8"
ENV LC_CTYPE="en_US.UTF-8"
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN apt-get update && apt-get upgrade -y
RUN apt-get -y install apt-utils locales-all locales vim
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get install -y build-essential \
  python3-pip python-is-python3 python3-psycopg2
RUN pip install --upgrade pip && pip install pipenv
WORKDIR /app/
COPY --chown=www-data:www-data . ./
RUN pipenv install --system --deploy
USER www-data 
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
