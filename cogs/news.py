import discord
from discord.ext import commands
from discord import app_commands
from utils.api import GamingNewsBot

class NewsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api = GamingNewsBot()

    @app_commands.command(name="latestnews", description="Get the latest gaming news")
    @app_commands.describe(limit="Number of games to show (max 10, default 5)")
    async def latest_news(self, interaction: discord.Interaction, limit: int = 5):
        """Slash command: Fetch latest gaming news"""
        await interaction.response.defer()
        
        try:
            if limit > 10:
                limit = 10
            elif limit < 1:
                limit = 1
            
            news_list = await self.api.fetch_latest_games(limit=limit)
            
            if not news_list:
                await interaction.followup.send("⚠️ No news found right now.", ephemeral=True)
                return

            embed = discord.Embed(
                title="📰 Latest Gaming News",
                description=f"Here are the top {len(news_list)} latest games!",
                color=discord.Color.purple()
            )
            
            for i, article in enumerate(news_list, 1):
                title = article.get("title", "Unknown Game")
                url = article.get("game_url", "")
                genre = article.get("genre", "Unknown")
                platform = article.get("platform", "PC")
                short_desc = article.get("short_description", "")
                
                value = f"**Genre:** {genre} | **Platform:** {platform}"
                if short_desc:
                    desc = short_desc[:80] + "..." if len(short_desc) > 80 else short_desc
                    value += f"\n{desc}"
                if url:
                    value += f"\n[🎮 Play Now]({url})"
                
                embed.add_field(
                    name=f"{i}. {title}",
                    value=value,
                    inline=False
                )
            
            embed.set_footer(text="Data from MMOBomb API")
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error in latest_news: {e}")
            await interaction.followup.send("❌ Something went wrong fetching the news!", ephemeral=True)
        finally:
            await self.api.close_session()

    @app_commands.command(name="setchannel", description="Set channel for auto news updates")
    @app_commands.describe(channel="Channel to send auto news to (optional, defaults to current channel)")
    async def set_news_channel(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Slash command: Set the channel for auto news"""
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You need 'Manage Channels' permission to use this!", ephemeral=True)
            return
        
        if channel is None:
            channel = interaction.channel
        
        self.bot.news_channel_id = channel.id
        
        embed = discord.Embed(
            title="✅ News Channel Set!",
            description=f"Auto news will now be posted in {channel.mention}",
            color=discord.Color.green()
        )
        embed.add_field(
            name="ℹ️ Info", 
            value="New games will be automatically posted every 2 hours!",
            inline=False
        )
        embed.add_field(
            name="💡 Tip",
            value="Use `/latestnews` to manually check for news anytime!",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="searchgame", description="Search for a specific game")
    @app_commands.describe(game_name="Name of the game to search for")
    async def search_game(self, interaction: discord.Interaction, game_name: str):
        """Slash command: Search for a specific game"""
        await interaction.response.defer()
        
        try:
            games = await self.api.fetch_games_list()
            
            if not games:
                await interaction.followup.send("❌ Could not fetch games list right now!", ephemeral=True)
                return
            
            matching_games = [
                game for game in games 
                if game_name.lower() in game.get("title", "").lower()
            ]
            
            if not matching_games:
                await interaction.followup.send(f"❌ No games found matching '{game_name}'", ephemeral=True)
                return
            
            # Take the first 5 matches
            matching_games = matching_games[:5]
            
            embed = discord.Embed(
                title=f"🔍 Search Results for '{game_name}'",
                description=f"Found {len(matching_games)} matching games:",
                color=discord.Color.blue()
            )
            
            for game in matching_games:
                title = game.get("title", "Unknown")
                genre = game.get("genre", "Unknown")
                platform = game.get("platform", "PC")
                game_id = game.get("id", "N/A") 
                url = game.get("game_url", "")
                
                value = f"**Genre:** {genre} | **Platform:** {platform} | **ID:** {game_id}"
                if url:
                    value += f"\n[🎮 Play Now]({url})"
                
                embed.add_field(name=title, value=value, inline=False)
            
            embed.set_footer(text="💡 Tip: Use /gameinfo <ID> to get detailed info about any game!")
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error in search_game: {e}")
            await interaction.followup.send("❌ Error searching for games!", ephemeral=True)
        finally:
            await self.api.close_session()

    @app_commands.command(name="newsoff", description="Turn off auto news for this server")
    async def turn_off_news(self, interaction: discord.Interaction):
        """Slash command: Turn off auto news"""
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You need 'Manage Channels' permission to use this!", ephemeral=True)
            return
        
        self.bot.news_channel_id = None
        
        embed = discord.Embed(
            title="🔕 Auto News Disabled",
            description="Auto news updates have been turned off for this server.",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="💡 To re-enable",
            value="Use `/setchannel` to set up auto news again!",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(NewsCog(bot))