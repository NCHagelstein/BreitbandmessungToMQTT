FROM cruizba/ubuntu-dind:latest


RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip install paho-mqtt
RUN mkdir /app
RUN mkdir /app/messprotokolle

COPY breitband.py /app/breitband.py
#COPY ./images /images
#COPY ./entrypoint.sh /entrypoint.sh

#ENTRYPOINT ["tini", "--", "/entrypoint.sh"]
CMD ["python3","/app/breitband.py"]