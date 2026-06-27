import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration
RULES_CHANNEL_ID = None
PRIVATE_BOTS_CHANNEL_ID = None
ACCOUNT_AGE_DAYS = 30
EXEMPT_USERS = set()  # Store exempt user IDs

class KickButtons(discord.ui.View):
    def __init__(self, user_id, user_name):
        super().__init__()
        self.user_id = user_id
        self.user_name = user_name

    @discord.ui.button(label="Kick User", style=discord.ButtonStyle.red)
    async def kick_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            guild = interaction.guild
            user = await guild.fetch_member(self.user_id)
            
            await user.kick(reason="Manual review - Rule 12 violation (no profile picture)")
            
            await interaction.response.send_message(
                f"✅ Kicked {self.user_name} for Rule 12 violation.",
                ephemeral=True
            )
            
            # Log to rules channel
            rules_channel = bot.get_channel(RULES_CHANNEL_ID)
            if rules_channel:
                embed = discord.Embed(
                    title="User Kicked",
                    description=f"**User:** {self.user_name} ({self.user_id})\n**Reason:** Manual review - Rule 12 violation (no profile picture)",
                    color=discord.Color.red()
                )
                await rules_channel.send(embed=embed)
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I don't have permission to kick this user.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(
                f"❌ Error kicking user: {e}",
                ephemeral=True
            )

    @discord.ui.button(label="Keep User", style=discord.ButtonStyle.green)
    async def keep_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"✅ Approved {self.user_name} for server.",
            ephemeral=True
        )
        
        # Log to rules channel
        rules_channel = bot.get_channel(RULES_CHANNEL_ID)
        if rules_channel:
            embed = discord.Embed(
                title="User Approved",
                description=f"**User:** {self.user_name} ({self.user_id})\n**Reason:** Manually approved by moderator",
                color=discord.Color.green()
            )
            await rules_channel.send(embed=embed)


async def check_member(member: discord.Member, channel: discord.TextChannel):
    """Check member profile and take appropriate action"""
    
    # Get current time and account creation time
    now = datetime.now(timezone.utc)
    account_age = now - member.created_at
    account_age_days = account_age.days
    
    # Check conditions
    is_old_enough = account_age_days >= ACCOUNT_AGE_DAYS
    has_pfp = member.avatar is not None
    
    # Prepare embed with results
    embed = discord.Embed(
        title="Member Screening Results",
        description=f"**User:** {member.mention} ({member})\n**User ID:** {member.id}",
        color=discord.Color.blue(),
        timestamp=now
    )
    
    embed.add_field(
        name="Account Age",
        value=f"{'✅' if is_old_enough else '❌'} {account_age_days} days old (Minimum: {ACCOUNT_AGE_DAYS} days)",
        inline=False
    )
    embed.add_field(
        name="Profile Picture",
        value=f"{'✅' if has_pfp else '❌'} {'Has custom avatar' if has_pfp else 'No custom avatar'}",
        inline=False
    )
    
    # Determine action
    if not is_old_enough:
        # Account too new - automatic kick
        embed.color = discord.Color.red()
        embed.title = "Member Kicked - Account Too New"
        embed.add_field(
            name="Action Taken",
            value="**Kicked** for violating Rule 12 (account < 30 days)",
            inline=False
        )
        
        try:
            await member.kick(reason="Rule 12 violation: Account less than 30 days old")
            await channel.send(embed=embed)
        except discord.Forbidden:
            embed.add_field(name="Error", value="Failed to kick - insufficient permissions", inline=False)
            await channel.send(embed=embed)
            
    elif is_old_enough and not has_pfp:
        # Account old enough but no profile picture - manual review
        embed.color = discord.Color.gold()
        embed.title = "Member Needs Manual Review"
        embed.add_field(
            name="Action Taken",
            value="**Pending manual review** - No profile picture",
            inline=False
        )
        
        await channel.send(embed=embed)
        
        # Send to private-bots channel
        private_bots = bot.get_channel(PRIVATE_BOTS_CHANNEL_ID)
        if private_bots:
            review_embed = discord.Embed(
                title="⚠️ Manual Member Review Required",
                description=f"**User:** {member.mention} ({member})\n**User ID:** {member.id}",
                color=discord.Color.gold(),
                timestamp=now
            )
            review_embed.add_field(name="Account Age", value=f"{account_age_days} days ✅", inline=True)
            review_embed.add_field(name="Profile Picture", value="Missing ❌", inline=True)
            
            await private_bots.send(embed=review_embed, view=KickButtons(member.id, str(member)))
            
    else:
        # All checks passed - account old enough and has profile picture
        embed.color = discord.Color.green()
        embed.title = "Member Passed Screening"
        embed.add_field(
            name="Action Taken",
            value="**Approved** - Member meets all requirements ✅",
            inline=False
        )
        
        await channel.send(embed=embed)


@bot.event
async def on_ready():
    """Bot startup event"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.event
async def on_member_join(member: discord.Member):
    """Handle new member join"""
    global RULES_CHANNEL_ID, PRIVATE_BOTS_CHANNEL_ID
    
    # Check if user is exempt from scanning
    if member.id in EXEMPT_USERS:
        print(f"User {member} is exempt from screening")
        return
    
    # Set channel IDs if not already set
    if RULES_CHANNEL_ID is None or PRIVATE_BOTS_CHANNEL_ID is None:
        for channel in member.guild.text_channels:
            if "general" in channel.name.lower() and RULES_CHANNEL_ID is None:
                RULES_CHANNEL_ID = channel.id
            if "private-bots" in channel.name.lower():
                PRIVATE_BOTS_CHANNEL_ID = channel.id
    
    # Get the channel to send messages to
    channel = None
    for ch in member.guild.text_channels:
        if ch.permissions_for(member.guild.me).send_messages:
            channel = ch
            break
    
    if channel is None:
        print(f"No suitable channel found to send screening results for {member}")
        return
    
    try:
        await check_member(member, channel)
    except Exception as e:
        print(f"Error checking member {member}: {e}")
        error_embed = discord.Embed(
            title="Error During Screening",
            description=f"An error occurred while screening {member.mention}. Please review manually.",
            color=discord.Color.red()
        )
        await channel.send(embed=error_embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx, rules_channel: discord.TextChannel, private_bots_channel: discord.TextChannel):
    """Setup the channels for screening results and manual reviews"""
    global RULES_CHANNEL_ID, PRIVATE_BOTS_CHANNEL_ID
    
    RULES_CHANNEL_ID = rules_channel.id
    PRIVATE_BOTS_CHANNEL_ID = private_bots_channel.id
    
    embed = discord.Embed(
        title="✅ Channels Configured",
        description=f"Rules channel: {rules_channel.mention}\nPrivate bots channel: {private_bots_channel.mention}",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def scan(ctx, member: discord.Member):
    """Manually scan a specific user"""
    await check_member(member, ctx.channel)

@bot.command()
@commands.has_permissions(administrator=True)
async def scanall(ctx):
    """Scan all members in the server"""
    
    if PRIVATE_BOTS_CHANNEL_ID is None:
        await ctx.send("❌ Private bots channel not configured. Use `!setup` first.")
        return
    
    # Start scanning
    status_embed = discord.Embed(
        title="🔍 Scanning All Members",
        description="Scanning server members... This may take a while.",
        color=discord.Color.blue()
    )
    status_msg = await ctx.send(embed=status_embed)
    
    passed = 0
    failed = 0
    private_bots = bot.get_channel(PRIVATE_BOTS_CHANNEL_ID)
    
    try:
        async for member in ctx.guild.fetch_members(limit=None):
            # Skip bot accounts
            if member.bot:
                continue
            
            # Check account age and pfp
            now = datetime.now(timezone.utc)
            account_age = now - member.created_at
            account_age_days = account_age.days
            
            is_old_enough = account_age_days >= ACCOUNT_AGE_DAYS
            has_pfp = member.avatar is not None
            
            # If should be kicked (old enough check + pfp check)
            if not is_old_enough or (is_old_enough and not has_pfp):
                failed += 1
                
                # Send to private-bots for verification
                if private_bots:
                    review_embed = discord.Embed(
                        title="⚠️ Member Needs Review (Scanall)",
                        description=f"**User:** {member.mention} ({member})\n**User ID:** {member.id}",
                        color=discord.Color.gold(),
                        timestamp=now
                    )
                    
                    if not is_old_enough:
                        review_embed.add_field(
                            name="Issue",
                            value=f"Account too new ({account_age_days} days old, minimum {ACCOUNT_AGE_DAYS})",
                            inline=False
                        )
                    else:
                        review_embed.add_field(
                            name="Issue",
                            value="No profile picture",
                            inline=False
                        )
                    
                    review_embed.add_field(name="Account Age", value=f"{account_age_days} days", inline=True)
                    review_embed.add_field(name="Profile Picture", value="✅" if has_pfp else "❌", inline=True)
                    
                    await private_bots.send(embed=review_embed, view=KickButtons(member.id, str(member)))
            else:
                # Passed all checks
                passed += 1
                
                # Send to main channel
                pass_embed = discord.Embed(
                    title="✅ Member Passed Scanall",
                    description=f"**User:** {member.mention} ({member})",
                    color=discord.Color.green()
                )
                pass_embed.add_field(name="Account Age", value=f"{account_age_days} days ✅", inline=True)
                pass_embed.add_field(name="Profile Picture", value="✅", inline=True)
                
                await ctx.send(embed=pass_embed)
        
        # Send final summary
        summary_embed = discord.Embed(
            title="✅ Scanall Complete",
            description=f"**Passed:** {passed}\n**Needs Review:** {failed}",
            color=discord.Color.green()
        )
        summary_embed.add_field(
            name="Total Members",
            value=f"{passed + failed}",
            inline=False
        )
        summary_embed.add_field(
            name="Next Steps",
            value=f"Check {private_bots.mention} for {failed} member(s) needing review",
            inline=False
        )
        
        await status_msg.edit(embed=summary_embed)
        
    except Exception as e:
        error_embed = discord.Embed(
            title="❌ Error During Scanall",
            description=f"Error: {str(e)}",
            color=discord.Color.red()
        )
        await status_msg.edit(embed=error_embed)



    """Check bot latency"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Bot latency: **{latency}ms**",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def allow(ctx, user_id: int):
    """Exempt a user from screening"""
    global EXEMPT_USERS
    
    EXEMPT_USERS.add(user_id)
    
    try:
        user = await bot.fetch_user(user_id)
        username = str(user)
    except:
        username = f"User {user_id}"
    
    embed = discord.Embed(
        title="✅ User Exempted",
        description=f"**User:** {username} (ID: {user_id})\n**Status:** Exempt from screening",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)


# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in .env file")
        print("Please create a .env file with: DISCORD_TOKEN=your_token_here")
    else:
        bot.run(TOKEN)
