FROM python:3.9.2

# System deps:
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
# Project initialization:
RUN poetry install

EXPOSE 8080

COPY ./ /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]