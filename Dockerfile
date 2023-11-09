FROM python:3.10-slim

EXPOSE 8000

ENV HOME /with_mongo

WORKDIR $HOME

COPY requirements.txt .
RUN python3 -m pip install --no-cache -r requirements.txt

ENV DB_HOST="mongo"
ENV DB_PORT="27017"

COPY . .

CMD python3 -m uvicorn main:app --reload -h 0.0.0.0 -p 8000