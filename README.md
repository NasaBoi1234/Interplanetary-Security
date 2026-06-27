# Discord Member Screening Bot

A Discord bot that automatically screens new members based on account age and profile picture.

## Features

✅ **Automatic Screening**
- Checks account age (30 days minimum)
- Checks for custom profile picture
- Automatically kicks users with accounts < 30 days old
- Flags accounts without profile pictures for manual review

✅ **Commands**
- `!ping` - Check bot status and latency
- `!setup <rules_channel> <private_bots_channel>` - Configure channels
- `!scan <@user>` - Manually scan a user
- `!allow <user_id>` - Exempt a user from screening

✅ **24/7 Hosting**
- Hosted on Railway (free)
- Runs continuously without needing your computer on
- Full logging and audit trail

## Setup

### Local Development

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

4. Run the bot:
   ```bash
   python discord_screening_bot_simple.py
   ```

### Production (Railway)

See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for detailed setup instructions.

## Commands

### User Commands
- `!ping` - Check bot responsiveness

### Admin Commands
- `!setup <rules_channel> <private_bots_channel>` - Configure screening channels
- `!scan <@user>` - Manually screen a user
- `!allow <user_id>` - Exempt a user from automatic screening

## Configuration

Edit `discord_screening_bot_simple.py` to change:
- `ACCOUNT_AGE_DAYS` - Minimum account age (default: 30)

## How It Works

1. **New member joins**
   - Bot checks account age
   - Bot checks for profile picture
   
2. **Account < 30 days old**
   - ❌ Automatically kicked
   
3. **Account ≥ 30 days old, no profile picture**
   - ⚠️ Manual review sent to #private-bots
   - Moderators can approve or kick
   
4. **Account ≥ 30 days old, has profile picture**
   - ✅ Automatically approved

## Requirements

- Python 3.10+
- discord.py 2.4.0+
- python-dotenv 1.0.0+

## License

MIT License

## Support

For issues or questions:
1. Check the [HOSTING_GUIDE.md](HOSTING_GUIDE.md)
2. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md)
3. Review the logs in Railway dashboard

## Discord Permissions

The bot requires:
- Send Messages
- Embed Links
- Kick Members
- Read Message History

Make sure the bot's role is high enough to kick members!
