import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all available bot commands")
    async def help_command(self, interaction: discord.Interaction):
        """Slash command: shows a comprehensive help menu"""
        embed = discord.Embed(
            title="🆘 Gaming Bot Help Menu",
            description="Here are all the commands you can use:",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="📰 News Commands",
            value=(
                "• `/latestnews [limit]` - Get latest gaming news\n"
                "• `/setchannel [channel]` - Set auto-news channel\n"
                "• `/searchgame <name>` - Search for a specific game"
            ),
            inline=False
        )

        embed.add_field(
            name="🎮 Game Info Commands",
            value=(
                "• `/gameinfo <id>` - Get detailed game info by ID\n"
                "• `/topgames [category] [limit]` - Show top games\n"
                "• `/randomgame` - Get a random game recommendation"
            ),
            inline=False
        )

        embed.add_field(
            name="📢 Channel Management",
            value=(
                "• `/create_channel <name>` - Create a new text channel\n"
                "• `/delete_channel <name>` - Delete an existing channel\n"
                "• `/list_channels` - List all server text channels"
            ),
            inline=False
        )

        # Utility Commands
        embed.add_field(
            name="🔧 Utility Commands", 
            value=(
                "• `/help` - Show this help menu\n"
                "• `/about` - Learn about this bot\n"
                "• `/ping` - Check bot response time"
            ),
            inline=False
        )

        embed.add_field(
            name="💡 Pro Tips",
            value=(
                "• Auto news updates every 2 hours when channel is set\n"
                "• Use game IDs from `/topgames` with `/gameinfo`\n"
                "• Categories: mmorpg, shooter, moba, battle-royale, etc."
            ),
            inline=False
        )

        embed.set_footer(text="🤖 Built with discord.py | Use slash commands (/)")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user else None)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="about", description="Learn about this gaming bot")
    async def about(self, interaction: discord.Interaction):
        """Slash command: about the bot"""
        embed = discord.Embed(
            title="🤖 About Gaming News Bot",
            description="Your ultimate gaming companion for the latest news and game info!",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="✨ Features",
            value=(
                "• Real-time gaming news from MMOBomb\n"
                "• Detailed game information and stats\n"
                "• Automatic news updates every 2 hours\n"
                "• Game search and recommendations\n"
                "• Channel management tools"
            ),
            inline=False
        )
        
        embed.add_field(
            name="📊 Bot Stats",
            value=(
                f"• Servers: {len(self.bot.guilds)}\n"
                f"• Users: {sum(guild.member_count for guild in self.bot.guilds)}\n"
                f"• Commands: {len([cmd for cmd in self.bot.tree.walk_commands()])}"
            ),
            inline=True
        )
        
        embed.add_field(
            name="🔗 Data Source",
            value="[MMOBomb API](https://www.mmobomb.com/api)",
            inline=True
        )
        
        embed.add_field(
            name="⚡ Version",
            value="v2.0 - Slash Commands",
            inline=True
        )

        embed.set_footer(text="Made with ❤️ using discord.py")
        embed.set_thumbnail(url=self.bot.user.display_avatar.url if self.bot.user else None)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ping", description="Check the bot's response time")
    async def ping(self, interaction: discord.Interaction):
        """Slash command: check bot latency"""
        latency = round(self.bot.latency * 1000)
        
        if latency < 100:
            color = discord.Color.green()
            status = "Excellent"
            emoji = "🟢"
        elif latency < 200:
            color = discord.Color.yellow()
            status = "Good"
            emoji = "🟡"
        else:
            color = discord.Color.red()
            status = "Poor"
            emoji = "🔴"

        embed = discord.Embed(
            title=f"{emoji} Pong!",
            description=f"**Latency:** {latency}ms\n**Status:** {status}",
            color=color
        )
        
        embed.set_footer(text="Response time to Discord API")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))