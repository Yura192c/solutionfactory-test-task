FROM python:3.10.10

WORKDIR /solutionfactory-test-task

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore


RUN pip install --upgrade pip

COPY Pipfile Pipfile.lock /solutionfactory-test-task/
RUN pip install pipenv && pipenv install --system

COPY . /solutionfactory-test-task/


RUN #python manage.py migrate
RUN python manage.py collectstatic --no-input

# copy entrypoint.sh
COPY ./entrypoint.sh /entrypoint.sh
# copy project
COPY . .
# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
