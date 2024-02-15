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
# https://github.com/flairNLP/flair/issues/1869#issuecomment-699638308
RUN  pip install --no-cache-dir torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html && \
     pip install --no-cache-dir flair==0.6.1 && \
     pip install --no-cache-dir transformers==3.3.1 && \
     pip install --no-cache-dir sentence-transformers==0.3.8

# Create the model directory.
RUN mkdir /root/model

# Copies your Flair model to the model directory on the image.
COPY model/final-model.pt /root/model/final-model.pt
COPY app/app.py /root/app.py

# At bootup, FASTAPI will execute the app.py file and the app function.
# In short, it will launch the endpoint whenever the container is launched.
CMD exec uvicorn --host 0.0.0.0 --port ${PORT} app:app