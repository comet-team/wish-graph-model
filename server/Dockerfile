FROM python:latest
COPY ./ ./
RUN pip install --upgrade pip
RUN pip install requests asyncio flask quart pandas
EXPOSE 8081
CMD ["python", "./quart_server.py"]