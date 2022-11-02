# Escape from Tarkov wiki bot

[![Add to Discord](https://img.shields.io/static/v1?label=&message=Add%20to%20Discord&color=7289da&logo=discord&labelColor=424549)](https://discord.com/api/oauth2/authorize?client_id=1037063623350161470&permissions=0&scope=bot)

1. `/tarkov search <query>`
1. `/tarkov details <item>`

## Quickstart

Click [this link](https://discord.com/api/oauth2/authorize?client_id=1037063623350161470&permissions=0&scope=bot) to add Tarkov bot to your Discord server!

## Running the bot

You may also download the code, alter it in any fashion and run the bot on your own computer.

1. Create a [Discord Application](https://discord.com/developers/applications), enable a bot account and create its authentication token.
2. Set your token as the `DISCORD_TOKEN` environment variable by running `export DISCORD_TOKEN=YOUR_TOKEN_HERE`.
3. Download and run the bot by executing the following:
   ```shell
   git clone https://github.com/fredericojordan/tarkovbot.git
   cd tarkovbot
   python tarkov_discord.py
   ```
4. Generate an invite link and add the bot to your Discord server.
