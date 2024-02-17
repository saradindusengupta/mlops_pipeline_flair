# Dockerfile
# python 3.8-slim with FastAPI pre-installed as a base image.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
WORKDIR /root

# Expose port 8080
ENV PORT=8080
EXPOSE ${PORT}

# Install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt /root/requirements.txt

# https://github.com/flairNLP/flair/issues/1869#issuecomment-699638308
RUN  pip install -r /root/requirements.txt

# Create the model directory.
RUN mkdir /root/model

# Copies your Flair model to the model directory on the image.
COPY model/final-model.pt /root/model/final-model.pt
COPY app/app.py /root/app.py

# At bootup, FASTAPI will execute the app.py file and the app function.
# In short, it will launch the endpoint whenever the container is launched.
CMD exec uvicorn --host 0.0.0.0 --port ${PORT} app:app