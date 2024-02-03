# Setup New HappyAIGen discord server

1. Enable Discord bot on your discord server.

2. Create a channel named `Happy_AIGen` in your server, and add some text channel to it.

3. Setup `env/discord_bot.env` with following example:

```bash
HAPPY_AIGEN_DISCORD_BOT_TOKEN="Token in https://discord.com/developers/applications/$BOT_ID/bot"
HAPPY_AIGEN_CATEGORY_NAME="Happy_AIGen, or other channel name you set in step2"
```

4. `python main.py`, keep running.

