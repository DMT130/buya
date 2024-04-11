FROM python:3.8.19

COPY . /app

RUN pip install -r requirments.txt

RUN pip install -r portal_sdk_2/requirements.txt

RUN pip install -r portal_sdk_2/.

ENTRYPOINT [ "uvicorn" "main:app" "--reload"]