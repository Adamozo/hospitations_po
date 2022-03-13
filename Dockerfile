FROM python:3.10

RUN mkdir /hospitations_po

COPY /hospitations_po /hospitations_po
COPY pyproject.toml /hospitations_po
COPY hospitations_po /hospitations_po/hospitations_po
COPY tests /hospitations_po/tests

WORKDIR /hospitations_po
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

RUN cd ./tests && \ 
    poetry run alembic -x data=true upgrade head

#RUN poetry run pytest -vv
