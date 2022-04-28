FROM python:latest
COPY ./ ./
RUN pip install --upgrade pip
RUN pip install requests asyncio flask quart pandas scipy numpy
EXPOSE 8081
CMD ["python", "./quart_server.py"]