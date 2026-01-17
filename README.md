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

## Onboarding Guilds (Servers)

1. Browse to [the installation page and add Hyperscout](https://discord.com/oauth2/authorize?client_id=1400445564264648796) to your server.
2. Ensure that Hyperscout has permissions to post messages in your intended destination text channel.
3. Copy the Server ID. (Instructions: [How to find a Server ID Number](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID#h_01HRSTXPS5FSFA0VWMY2CKGZXA))
4. Copy the Channel ID for the text channel that you'd like to use as a destination. (Instructions: [How to find a Channel ID Number](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID#h_01HRSTXPS5FMK2A5SMVSX4JW4E))
5. Follow the command in Configuring/Updating a Guild, substituting in your values collected earlier.

## Configuring/Updating a Guild

```shell
docker run --rm -v './data:/data' ghcr.io/adrianmace/hyperscout:latest set --guild-id '1234567890' --destination-channel-id '0987654321'
```

## Deleting a Guild

```shell
docker run --rm -v './data:/data' ghcr.io/adrianmace/hyperscout:latest delete --guild-id '1234567890'
```
