FROM python:3.12-slim
WORKDIR /app
COPY src /app/src
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin appuser
USER 10001:10001
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080
EXPOSE 8080
CMD ["python", "-m", "src.service"]
