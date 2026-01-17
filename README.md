# hyperscout

A simple Discord bot that notifies a text channel when people join voice channels.
It also cleans up its own messages at midnight UTC.

## Getting Started

To run the bot, you can use the following docker command:

```bash
docker run -d \
  --name 'hyperscout' \
  -e HYPERSCOUT_BOT_TOKEN="your_bot_token" \
  -e HYPERSCOUT_DATABASE_PATH="/data/hyperscout.db" \
  -v './data:/data' \
  ghcr.io/adrianmace/hyperscout:latest
```

## Environment Variables

| Variable                          | Description                                          | Default Value         | Required |
| --------------------------------- | ---------------------------------------------------- | --------------------- | -------- |
| `HYPERSCOUT_BOT_TOKEN`            | The Discord bot token.                               | `None`                | True     |
| `HYPERSCOUT_DATABASE_PATH`        | The path on disk where the database will be stored.  | `/data/hyperscout.db` | False    |

## Onboarding Servers

1. Browse to [the installation page and add Hyperscout](https://discord.com/oauth2/authorize?client_id=1400445564264648796) to your server.
2. Ensure that Hyperscout has appropriate server permissions to post messages in your intended destination channel.
3. As the server owner, run the `/configure` slash command to configure the destination channel.
