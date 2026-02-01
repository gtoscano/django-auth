FROM python:3.13-trixie
LABEL AUTHOR "Greogrio Toscano <gtoscano@fastmail.com>"
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  DEBIAN_FRONTEND=noninteractive \
  LANG="en_US.UTF-8" \
  LC_ALL="en_US.UTF-8" \
  LC_CTYPE="en_US.UTF-8"

RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN apt-get update && apt-get upgrade -y && apt-get -y install apt-utils locales-all locales vim
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN apt-get install -y build-essential \
  python3-pip python-is-python3
WORKDIR /app/
COPY Pipfile ./
RUN pip install --upgrade pip && pip install --no-cache-dir pipenv
RUN pipenv lock --clear
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=www-data:www-data . ./
USER www-data 
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
