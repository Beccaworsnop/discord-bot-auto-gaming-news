import discord
from discord.ext import commands
from discord import app_commands
from utils.api import GamingNewsBot

class GameInfoCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api = GamingNewsBot()

    @app_commands.command(name="gameinfo", description="Get detailed info about a specific game by ID")
    @app_commands.describe(game_id="The game ID number (use /topgames to find IDs)")
    async def gameinfo(self, interaction: discord.Interaction, game_id: int):
        """Slash command: fetches and shows detailed info about a game by ID"""
        await interaction.response.defer()
        
        try:
            game_data = await self.api.fetch_game_details(game_id)
            
            if not game_data or "error" in game_data:
                await interaction.followup.send(f"❌ Game with ID {game_id} not found!", ephemeral=True)
                return
            
            title = game_data.get("title", "Unknown Game")
            description = game_data.get("description", "No description available")
            genre = game_data.get("genre", "Unknown")
            platform = game_data.get("platform", "PC")
            publisher = game_data.get("publisher", "Unknown")
            developer = game_data.get("developer", "Unknown") 
            release_date = game_data.get("release_date", "Unknown")
            game_url = game_data.get("game_url", "")
            thumbnail = game_data.get("thumbnail", "")
            
            embed = discord.Embed(
                title=f"🎮 {title}",
                description=description[:500] + "..." if len(description) > 500 else description,
                color=discord.Color.blue(),
                url=game_url if game_url else None
            )
            
            embed.add_field(name="🎯 Genre", value=genre, inline=True)
            embed.add_field(name="💻 Platform", value=platform, inline=True) 
            embed.add_field(name="📅 Release Date", value=release_date, inline=True)
            embed.add_field(name="🏢 Publisher", value=publisher, inline=True)
            embed.add_field(name="👨‍💻 Developer", value=developer, inline=True)
            embed.add_field(name="🆔 Game ID", value=str(game_id), inline=True)
            
            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            
            if game_url:
                embed.add_field(name="🔗 Play Now", value=f"[Click here to play]({game_url})", inline=False)
            
            embed.set_footer(text="Data from MMOBomb API")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error in gameinfo: {e}")
            await interaction.followup.send("❌ Error fetching game info!", ephemeral=True)
        finally:
            await self.api.close_session()

    @app_commands.command(name="topgames", description="Show top games by category")
    @app_commands.describe(
        category="Game category to filter by",
        limit="Number of games to show (max 10)"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name="All Games", value=""),
        app_commands.Choice(name="MMORPG", value="mmorpg"),
        app_commands.Choice(name="Shooter", value="shooter"), 
        app_commands.Choice(name="MOBA", value="moba"),
        app_commands.Choice(name="Battle Royale", value="battle-royale"),
        app_commands.Choice(name="Strategy", value="strategy"),
        app_commands.Choice(name="Fighting", value="fighting"),
        app_commands.Choice(name="Action RPG", value="action-rpg"),
        app_commands.Choice(name="Card Game", value="card"),
        app_commands.Choice(name="Racing", value="racing"),
        app_commands.Choice(name="Sports", value="sports")
    ])
    async def topgames(self, interaction: discord.Interaction, category: str = "", limit: int = 5):
        """Slash command: lists top games by category"""
        await interaction.response.defer()
        
        try:
            if limit > 10:
                limit = 10
            
            games = await self.api.fetch_games_list(category=category if category else None)
            
            if not games:
                await interaction.followup.send("❌ No games found in this category!", ephemeral=True)
                return
            
            games = games[:limit]
            
            category_name = category.title().replace("-", " ") if category else "All Categories"
            
            embed = discord.Embed(
                title=f"🔥 Top {category_name} Games",
                description=f"Here are the top {len(games)} games:",
                color=discord.Color.green()
            )
            
            for i, game in enumerate(games, 1):
                title = game.get("title", "Unknown")
                genre = game.get("genre", "Unknown")
                platform = game.get("platform", "PC")
                game_id = game.get("id", "N/A")
                url = game.get("game_url", "")
                
                value = f"**Genre:** {genre} | **Platform:** {platform} | **ID:** {game_id}"
                if url:
                    value += f"\n[🎮 Play Now]({url})"
                
                embed.add_field(
                    name=f"{i}. {title}",
                    value=value,
                    inline=False
                )
            
            embed.set_footer(text="💡 Tip: Use /gameinfo <ID> to get detailed info about any game!")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error in topgames: {e}")
            await interaction.followup.send("❌ Error fetching top games!", ephemeral=True)
        finally:
            await self.api.close_session()

    @app_commands.command(name="randomgame", description="Get a random game recommendation")
    async def randomgame(self, interaction: discord.Interaction):
        """Slash command: get a random game"""
        await interaction.response.defer()
        
        try:
            import random
            games = await self.api.fetch_games_list()
            
            if not games:
                await interaction.followup.send("❌ No games available right now!", ephemeral=True)
                return
            
            random_game = random.choice(games)
            
            title = random_game.get("title", "Unknown Game")
            genre = random_game.get("genre", "Unknown")
            platform = random_game.get("platform", "PC")
            game_id = random_game.get("id", "N/A")
            url = random_game.get("game_url", "")
            thumbnail = random_game.get("thumbnail", "")
            short_desc = random_game.get("short_description", "No description available")
            
            embed = discord.Embed(
                title=f"🎲 Random Game: {title}",
                description=short_desc[:300] + "..." if len(short_desc) > 300 else short_desc,
                color=discord.Color.random()
            )
            
            embed.add_field(name="🎯 Genre", value=genre, inline=True)
            embed.add_field(name="💻 Platform", value=platform, inline=True)
            embed.add_field(name="🆔 Game ID", value=str(game_id), inline=True)
            
            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            
            if url:
                embed.add_field(name="🔗 Play Now", value=f"[Click here to play]({url})", inline=False)
            
            embed.set_footer(text="💡 Use /gameinfo to get more details about this game!")
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            print(f"Error in randomgame: {e}")
            await interaction.followup.send("❌ Error getting random game!", ephemeral=True)
        finally:
            await self.api.close_session()

async def setup(bot: commands.Bot):
    await bot.add_cog(GameInfoCog(bot))