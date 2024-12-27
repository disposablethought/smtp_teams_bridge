FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY smtp_to_teams.py .

# Create a non-root user
RUN useradd -m -r -u 1000 appuser
USER appuser

ENV PYTHONUNBUFFERED=1

CMD ["python", "smtp_to_teams.py"]
