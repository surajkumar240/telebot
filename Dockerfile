FROM python:3.7

RUN pip install flask requests

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/bot.py
CMD ["-p","5555:4444"]
