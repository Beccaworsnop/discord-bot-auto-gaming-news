import discord
from discord.ext import commands
from discord import app_commands

class ChannelCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="create_channel", description="Create a new text channel in the server")
    @app_commands.describe(channel_name="Name of the channel to create")
    async def create_channel(self, interaction: discord.Interaction, channel_name: str):
        """Slash command: Create a new text channel"""

        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You need 'Manage Channels' permission to use this!", ephemeral=True)
            return
        
        guild = interaction.guild
        
        clean_name = channel_name.lower().replace(" ", "-").replace("_", "-")
        
        existing_channel = discord.utils.get(guild.channels, name=clean_name)
        if existing_channel:
            await interaction.response.send_message(f"❌ Channel `{clean_name}` already exists.", ephemeral=True)
            return
        
        try:

            new_channel = await guild.create_text_channel(clean_name)
            
            embed = discord.Embed(
                title="✅ Channel Created!",
                description=f"Successfully created {new_channel.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="Channel Name", value=clean_name, inline=True)
            embed.add_field(name="Channel ID", value=new_channel.id, inline=True)
            embed.add_field(name="Created By", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to create channels!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error creating channel: {str(e)}", ephemeral=True)

    @app_commands.command(name="delete_channel", description="Delete an existing text channel")
    @app_commands.describe(channel="Channel to delete (mention or name)")
    async def delete_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Slash command: Delete a text channel"""

        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ You need 'Manage Channels' permission to use this!", ephemeral=True)
            return
        
        if channel.name in ['general', 'rules', 'announcements']:
            await interaction.response.send_message("❌ Cannot delete important server channels!", ephemeral=True)
            return
        
        try:
            channel_name = channel.name
            await channel.delete(reason=f"Deleted by {interaction.user}")
            
            embed = discord.Embed(
                title="🗑️ Channel Deleted!",
                description=f"Successfully deleted `#{channel_name}`",
                color=discord.Color.red()
            )
            embed.add_field(name="Deleted By", value=interaction.user.mention, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to delete that channel!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error deleting channel: {str(e)}", ephemeral=True)

    @app_commands.command(name="list_channels", description="List all text channels in the server")
    async def list_channels(self, interaction: discord.Interaction):
        """Slash command: List all text channels"""
        guild = interaction.guild
        text_channels = guild.text_channels
        voice_channels = guild.voice_channels
        
        if not text_channels:
            await interaction.response.send_message("❌ No text channels found in this server.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title=f"📋 Channels in {guild.name}",
            color=discord.Color.blue()
        )
        
        text_list = []
        for i, ch in enumerate(text_channels, 1):
            members = len([m for m in ch.members if not m.bot])
            text_list.append(f"{i}. {ch.mention} (`{ch.name}`) - {members} members")
        
        text_chunks = []
        current_chunk = ""
        for channel_info in text_list:
            if len(current_chunk + channel_info + "\n") > 1024:
                text_chunks.append(current_chunk.strip())
                current_chunk = channel_info + "\n"
            else:
                current_chunk += channel_info + "\n"
        if current_chunk.strip():
            text_chunks.append(current_chunk.strip())
        
        for i, chunk in enumerate(text_chunks):
            field_name = "💬 Text Channels" if i == 0 else f"💬 Text Channels (cont. {i+1})"
            embed.add_field(name=field_name, value=chunk, inline=False)
        
        if voice_channels:
            voice_summary = f"🔊 **Voice Channels:** {len(voice_channels)} total"
            embed.add_field(name="Voice Channels", value=voice_summary, inline=False)
        
        embed.set_footer(text=f"Total: {len(text_channels)} text channels • {len(voice_channels)} voice channels")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="channel_info", description="Get detailed information about a channel")
    @app_commands.describe(channel="Channel to get info about (optional, defaults to current channel)")
    async def channel_info(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        """Slash command: Get detailed channel information"""
        if channel is None:
            channel = interaction.channel
        
        embed = discord.Embed(
            title=f"📊 Channel Info: #{channel.name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="🆔 Channel ID", value=channel.id, inline=True)
        embed.add_field(name="📅 Created", value=f"<t:{int(channel.created_at.timestamp())}:R>", inline=True)
        embed.add_field(name="📍 Position", value=channel.position, inline=True)
        
        members = len([m for m in channel.members if not m.bot])
        bots = len([m for m in channel.members if m.bot])
        embed.add_field(name="👥 Members", value=f"{members} humans, {bots} bots", inline=True)
        
        topic = channel.topic if channel.topic else "No topic set"
        embed.add_field(name="📝 Topic", value=topic[:100] + "..." if len(topic) > 100 else topic, inline=False)
        
        perms = channel.permissions_for(interaction.user)
        perm_list = []
        if perms.manage_messages: perm_list.append("Manage Messages")
        if perms.manage_channels: perm_list.append("Manage Channels")
        if perms.send_messages: perm_list.append("Send Messages")
        if perms.read_messages: perm_list.append("Read Messages")
        
        embed.add_field(
            name="🔐 Your Permissions", 
            value=", ".join(perm_list[:4]) if perm_list else "Limited permissions",
            inline=False
        )
        
        embed.set_footer(text="Channel statistics")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelCog(bot))