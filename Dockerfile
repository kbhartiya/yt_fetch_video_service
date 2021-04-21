FROM python:3
RUN mkdir app
ADD app.py /app
RUN pip install -r requirements.txt
CMD [ "python", "./app/app.py --key <>" ]