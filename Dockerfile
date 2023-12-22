FROM python:3.10-slim AS buildstage

WORKDIR /usr/src/app

COPY . .

RUN pip install fastapi

RUN pip install "uvicorn[standard]"

ENV PORT=3000

EXPOSE ${PORT}

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]