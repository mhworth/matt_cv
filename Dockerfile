FROM mhworth/python-analysis-webapp
MAINTAINER Matt Hollingsworth mr.hworth@gmail.com

ENV PYTHONPATH=/opt/matt_cv
#RUN conda install python-memcached

ADD . /opt/matt_cv
WORKDIR /opt/matt_cv
RUN mkdir -p /var/www
RUN conda install dj-static

ENV DJANGO_SETTINGS_MODULE="matt_cv.settings_production"

RUN cd matt_cv && scripts/create.sh && /opt/matt_cv/manage.py collectstatic --noinput
EXPOSE 8000

CMD ["gunicorn", "--log-file=-", "-b", "0.0.0.0:8000", "-w", "2", "app"]



