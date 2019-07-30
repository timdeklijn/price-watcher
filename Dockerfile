FROM python:3
ADD price_watcher/ price_watcher/
ADD requirements.txt .
ADD bucket/ bucket/
RUN pip install -r requirements.txt
CMD [ "python", "-m", "price_watcher"]