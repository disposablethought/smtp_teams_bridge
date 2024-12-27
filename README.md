# SMTP to Teams Webhook Bridge

A simple service that accepts SMTP emails and forwards them to Microsoft Teams via webhooks.

## Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Teams webhook URL:
   ```
   TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/your-webhook-url-here
   SMTP_PORT=25  # Change if needed
   ```

3. Start the service:
   ```bash
   docker-compose up -d
   ```

## Usage

Configure your application to send SMTP emails to this service:

- SMTP Host: your-docker-host
- SMTP Port: 25 (or whatever you configured in .env)
- No authentication required

The service will:
1. Accept incoming emails
2. Convert them to Teams messages
3. Send them to your configured Teams webhook (webhook is now workflows)

## Features

- Runs as a Docker service
- Automatic restart on failure
- Converts email subject and body to Teams adaptive cards
- Supports both plain text and HTML emails
- Logging for monitoring and debugging

## Security Notes

- The service runs as a non-root user inside Docker
- No authentication is implemented - secure through network configuration
- Use in trusted networks only
