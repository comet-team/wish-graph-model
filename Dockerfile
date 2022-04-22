FROM python:latest
RUN pip install --upgrade pip
WORKDIR /server
COPY quart_server.py .
EXPOSE 8081
RUN pip install requests asyncio flask quart pandas
CMD ["python", "quart_server.py"]