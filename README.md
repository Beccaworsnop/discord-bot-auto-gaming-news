# 🎮 Discord Gaming News Bot

Hey so this is my Discord bot that automatically delivers the latest gaming news and provides comprehensive game information using the MMOBomb API. Perfect for gaming communities who want to stay up-to-date with new releases and game information which I am currently using on my server :)

## ✨ Features

### 📰 **Automatic News Updates**
- Auto-posts new games every 2 hours to your designated channel
- Rich embeds with game details, descriptions, and play links
- Smart filtering to avoid duplicate posts

### 🎯 **Game Information Commands**
- Detailed game information with screenshots and stats
- Top games by category (MMORPG, Shooter, MOBA, etc.)
- Random game recommendations
- Comprehensive game search functionality

### 🔧 **Server Management**
- Create and delete text channels
- List all server channels with member counts
- Detailed channel information and permissions

### 💬 **User-Friendly Interface**
- Modern slash commands (/) for easy use
- Interactive embeds with rich formatting
- Comprehensive help system
- Real-time bot status and latency checking

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- A Discord bot token
- Basic knowledge of Discord server management

### 2. Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Beccaworsnop/discord-bot-auto-gaming-news.git
cd discord-bot-auto-gaming-news
```

2. **Create environment file:**
Create a `.env` file in the root directory:
```env
DISCORD_TOKEN=your_discord_bot_token_here
```

4. **Run the bot:**
```bash
python bot.py
```

### 3. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Copy the bot token and add it to your `.env` file
5. Enable the following **Bot Permissions**:
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History
   - Manage Channels (optional, for channel management)

6. **Invite the bot** to your server using the OAuth2 URL generator with the above permissions.

## 📋 Command List

### 📰 **News Commands**
| Command | Description | Usage |
|---------|-------------|--------|
| `/latestnews` | Get latest gaming news | `/latestnews [limit]` |
| `/setchannel` | Set auto news channel | `/setchannel [#channel]` |
| `/newsoff` | Disable auto news | `/newsoff` |
| `/searchgame` | Search for specific games | `/searchgame <game name>` |

### 🎮 **Game Info Commands**
| Command | Description | Usage |
|---------|-------------|--------|
| `/gameinfo` | Detailed game information | `/gameinfo <game_id>` |
| `/topgames` | Top games by category | `/topgames [category] [limit]` |
| `/randomgame` | Random game recommendation | `/randomgame` |

### 🔧 **Channel Management**
| Command | Description | Usage |
|---------|-------------|--------|
| `/create_channel` | Create a new text channel | `/create_channel <name>` |
| `/delete_channel` | Delete an existing channel | `/delete_channel <#channel>` |
| `/list_channels` | List all server channels | `/list_channels` |
| `/channel_info` | Get channel details | `/channel_info [#channel]` |

### ℹ️ **Utility Commands**
| Command | Description | Usage |
|---------|-------------|--------|
| `/help` | Show all commands | `/help` |
| `/about` | Bot information | `/about` |
| `/ping` | Check bot latency | `/ping` |
| `/test` | Test bot functionality | `/test` |

## 🎯 How to Use

### Setting Up Auto News
1. Use `/setchannel` in your desired news channel
2. The bot will automatically post new games every 2 hours
3. Use `/newsoff` to disable auto updates

### Getting Game Information
1. Use `/topgames` to see popular games and their IDs
2. Use `/gameinfo <id>` to get detailed information about any game
3. Use `/searchgame <name>` to find specific games

### Managing Channels
1. Use `/create_channel <name>` to create new channels
2. Use `/list_channels` to see all server channels
3. Use `/delete_channel` to remove unwanted channels

## 🏗️ Project Structure

```
discord-gaming-bot/
├── bot.py                 # Main bot file
├── cogs/                  # Command modules
│   ├── __init__.py
│   ├── channels.py        # Channel management commands
│   ├── gameinfo.py        # Game information commands  
│   ├── help.py            # Help and utility commands
│   └── news.py            # News and auto-update commands
├── utils/                 # Utility modules
│   ├── __init__.py
│   └── api.py             # MMOBomb API wrapper
├── .env                   # Environment variables (create this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with the following:
```env
# Required: Your Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# Optional: Customize auto-update interval (default: 2 hours)
# NEWS_INTERVAL_HOURS=2
```


