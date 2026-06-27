# Discord Member Screening Bot

A Discord bot that automatically screens new members based on account age, profile picture, and bio.

## Features

✅ **Automatic member screening** when someone joins
- Checks if account is over 1 month old
- Checks if they have a custom profile picture
- Checks if they have a bio/about section

✅ **Smart actions based on profile**
- **Too new (<1 month)**: Instant kick with reason
- **Missing both PFP and bio**: Instant kick with reason
- **Missing one (PFP or bio)**: Asks for manual review in #private-bots with approve/kick buttons
- **All checks pass**: Posts approval message

✅ **Logging**: All actions logged to the channel

## Setup Instructions

### 1. Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Under TOKEN, click "Copy" to copy your bot token
5. Save this token - you'll need it soon

### 2. Set Bot Permissions

1. In Developer Portal, go to "OAuth2" → "URL Generator"
2. Select these scopes:
   - `bot`
3. Select these permissions:
   - `Send Messages`
   - `Embed Links`
   - `Read Message History`
   - `Kick Members`
4. Copy the generated URL and open it to invite the bot to your server

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env File

Create a file named `.env` in the same directory as the bot:

```
DISCORD_TOKEN=your_bot_token_here
```

Replace `your_bot_token_here` with the token you copied from Step 1.

### 5. Run the Bot

```bash
python discord_screening_bot.py
```

You should see:
```
Your Bot Name has connected to Discord!
Bot is in X guild(s)
Synced X command(s)
```

### 6. Configure Channels (First Time Only)

The bot will try to auto-detect a #general channel and #private-bots channel. To manually set them:

```
!setup_channels #channel-name #private-bots
```

Example:
```
!setup_channels #welcome #private-bots
```

## How It Works

### When a user joins:

```
Account < 1 month old
    ↓
    INSTANT KICK ❌

Account ≥ 1 month old
    ↓
    ├─ Has PFP + Has Bio
    │   ↓
    │   APPROVED ✅
    │
    ├─ Missing PFP + Missing Bio
    │   ↓
    │   INSTANT KICK ❌
    │
    └─ Has one, missing other
        ↓
        MANUAL REVIEW (in #private-bots with buttons)
```

## Commands

### `!setup_channels <rules_channel> <private_bots_channel>`
Configure which channels to use for logging. (Admin only)

**Example:**
```
!setup_channels #welcome #private-bots
```

### `!check_user <@user>`
Manually check a specific user's profile. (Admin only)

**Example:**
```
!check_user @UserName
```

## Configuration

Edit these values in the bot file to customize:

```python
ACCOUNT_AGE_DAYS = 30  # Change to require accounts older/newer than this
```

## Troubleshooting

### Bot doesn't respond to commands
- Make sure the bot has Send Messages permission
- Bot must be above the role it's trying to kick users with

### Bot can't kick users
- Move the bot's role higher in the role hierarchy
- Make sure bot has "Kick Members" permission

### Doesn't find #private-bots channel
- Manually run: `!setup_channels #general #private-bots`
- Replace with your actual channel names

### "No suitable channel found"
- The bot needs at least one text channel it has permission to send messages to
- Grant the bot Send Messages permission in at least one channel

## Channel Requirements

Make sure your server has:
- **A channel for screening results** (like #welcome or #general) - bot will post results here
- **#private-bots channel** - for manual review requests with buttons

## Permissions Needed

The bot requires:
- `Send Messages` - to post screening results
- `Embed Links` - to send formatted messages
- `Kick Members` - to remove rule-breaking members
- `Read Message History` - (optional, for context)

## What Gets Checked

### Account Age
- Discord account creation date
- Must be at least 30 days old (configurable)

### Profile Picture
- Checks if user has a custom avatar
- Default Discord avatars are not accepted

### Bio/About
- Checks if user has filled in their "About Me" section
- Empty bios are not accepted

## Notes

- The bot automatically checks members when they join - no setup needed after initial configuration
- Manual review messages have buttons to Kick or Keep the user
- All kicks include the rule violation in the audit log
- The bot works 24/7 as long as it's running

## Support

If you encounter issues:
1. Check that the bot has proper permissions
2. Verify the .env file has your correct token
3. Make sure channels are correctly set with `!setup_channels`
4. Check Discord server logs/audit log for any error messages
