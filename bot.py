import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

bot.news_channel_id = None

initial_extensions = [
    "cogs.news",
    "cogs.gameinfo", 
    "cogs.channels",
    "cogs.help"
]

@bot.event
async def on_ready():
    print(f"🤖 {bot.user} is online in {len(bot.guilds)} guilds!")
    
    if not auto_news_task.is_running():
        auto_news_task.start()
        print("📰 Auto news task started!")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
        
        for cmd in synced:
            print(f"  • /{cmd.name} - {cmd.description}")
            
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@bot.command(name="sync")
@commands.is_owner()
async def sync_commands(ctx):
    """Manually sync slash commands (owner only)"""
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Synced {len(synced)} commands!")
        print(f"Manual sync: {len(synced)} commands")
    except Exception as e:
        await ctx.send(f" Sync failed: {e}")
        print(f"Manual sync failed: {e}")

@bot.tree.command(name="test", description="Test if slash commands are working")
async def test_command(interaction: discord.Interaction):
    """Simple test command"""
    embed = discord.Embed(
        title="✅ Bot is Working!",
        description="Slash commands are functioning properly!",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command(name="debug")
@commands.is_owner()
async def debug_cogs(ctx):
    """Check what cogs are loaded"""
    loaded_cogs = list(bot.cogs.keys())
    all_commands = [cmd.name for cmd in bot.tree.walk_commands()]
    
    embed = discord.Embed(title="🔧 Debug Info", color=discord.Color.blue())
    embed.add_field(name="Loaded Cogs", value="\n".join(loaded_cogs) if loaded_cogs else "None", inline=False)
    embed.add_field(name="Slash Commands", value="\n".join(all_commands) if all_commands else "None", inline=False)
    embed.add_field(name="News Channel", value=bot.news_channel_id or "Not Set", inline=False)
    
    await ctx.send(embed=embed)

@tasks.loop(hours=2) 
async def auto_news_task():
    """Automatically post new gaming news"""
    if not bot.news_channel_id:
        print(" Auto news skipped  no channel set")
        return
    
    channel = bot.get_channel(bot.news_channel_id)
    if not channel:
        print(" Auto news skipped  channel not found")
        return
    
    try:
        from utils.api import GamingNewsBot
        api = GamingNewsBot()
        
        new_games = await api.get_new_games(limit=3)
        
        if new_games:
            embed = discord.Embed(
                title="🚨 **NEW GAMES ALERT!**",
                description="Fresh gaming news just dropped!",
                color=discord.Color.red()
            )
            
            for game in new_games:
                title = game.get("title", "Unknown Game")
                url = game.get("game_url", "")
                short_desc = game.get("short_description", "No description available")
                
                if len(short_desc) > 100:
                    short_desc = short_desc[:100] + "..."
                
                field_value = short_desc
                if url:
                    field_value += f"\n[🔗 Play Now]({url})"
                
                embed.add_field(
                    name=f"🎮 {title}",
                    value=field_value,
                    inline=False
                )
            
            embed.set_footer(text=f"Auto-update • Found {len(new_games)} new games")
            await channel.send(embed=embed)
            print(f"📰 Posted {len(new_games)} new games to channel {channel.name}")
        else:
            print("📰 No new games found")
        
        await api.close_session()
        
    except Exception as e:
        print(f"❌ Auto news error: {e}")

@bot.command(name="setchannel")
@commands.has_permissions(manage_channels=True)
async def set_news_channel_prefix(ctx, channel: discord.TextChannel = None):
    """Set the channel for auto news updates (prefix command backup)"""
    if channel is None:
        channel = ctx.channel
    
    bot.news_channel_id = channel.id
    await ctx.send(f" Auto news will be posted in {channel.mention}")

async def load_extensions():
    """Load all extensions"""
    for ext in initial_extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f" Failed to load {ext}: {e}")

async def main():
    """Main async function to run the bot"""
    if not DISCORD_TOKEN:
        return
    
    await load_extensions()
    
    try:
        await bot.start(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print(" Bot shutdown requested")
        await bot.close()
    except Exception as e:
        print(f"error: {e}")
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())