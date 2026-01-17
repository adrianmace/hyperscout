# hyperscout

A simple Discord bot that notifies a text channel when people join voice channels.
It also cleans up its own messages at midnight UTC.

## Getting Started

To run the bot, you can use the following docker command:

```bash
docker run -d \
  --name hyperscout \
  -e HYPERSCOUT_BOT_TOKEN="your_bot_token" \
  -e HYPERSCOUT_DESTINATION_CHANNEL_ID="your_channel_id" \
  ghcr.io/adrianmace/hyperscout:latest
```

## Environment Variables

| Variable                          | Description                                | Default Value |
| --------------------------------- | ------------------------------------------ | ------------- |
| `HYPERSCOUT_BOT_TOKEN`            | The Discord bot token.                     | `None`        |
| `HYPERSCOUT_DESTINATION_CHANNEL_ID` | The ID of the channel to send messages to. | `None`        |
