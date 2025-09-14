import aiohttp
import asyncio
from typing import Optional, List, Dict

MMO_API_BASE_URL = "https://www.mmobomb.com/api1"


class GamingNewsBot:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.news_cache: List[Dict] = []
        self.last_update = None
        self.previous_news_ids: set[int] = set()

    async def create_session(self):
        """Create aiohttp session if not already created"""
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)

    async def close_session(self):
        """Close aiohttp session if open"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def _make_request(self, url: str, params: Dict = None) -> Dict:
        """Make an HTTP request with error handling"""
        await self.create_session()
        
        try:
            async with self.session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data if data else {}
                else:
                    print(f"API request failed: {resp.status}")
                    return {}
        except asyncio.TimeoutError:
            print("Request timed out")
            return {}
        except Exception as e:
            print(f"Request error: {e}")
            return {}

    async def fetch_games_list(self, category: str = None, platform: str = None) -> List[Dict]:
        """Fetch list of games by category/platform"""
        url = f"{MMO_API_BASE_URL}/games"
        params: Dict[str, str] = {}
        
        if category:
            params["category"] = category
        if platform:
            params["platform"] = platform
            
        result = await self._make_request(url, params)
        return result if isinstance(result, list) else []

    async def fetch_game_details(self, game_id: int) -> Dict:
        """Fetch detailed info for a specific game"""
        url = f"{MMO_API_BASE_URL}/game"
        params = {"id": game_id}
        
        result = await self._make_request(url, params)
        return result if isinstance(result, dict) else {}

    async def fetch_latest_games(self, limit: int = 10) -> List[Dict]:
        """Fetch latest games (sorted by release date)"""
        url = f"{MMO_API_BASE_URL}/games"
        params = {"sort-by": "release-date"}
        
        result = await self._make_request(url, params)
        
        if isinstance(result, list) and result:
            return result[:limit]
        return []

    async def get_new_games(self, limit: int = 5) -> List[Dict]:
        """Get new games that were not cached before"""
        try:
            current_games = await self.fetch_latest_games(limit * 3)  
            new_games: List[Dict] = []
            current_ids: set[int] = set()

            for game in current_games:
                game_id = game.get("id")
                if not game_id:
                    continue
                    
                current_ids.add(game_id)
                
                if game_id not in self.previous_news_ids:
                    new_games.append(game)
                    
                if len(new_games) >= limit:
                    break

            self.previous_news_ids.update(current_ids)
            
            return new_games
            
        except Exception as e:
            print(f"Error getting new games: {e}")
            return []

    async def search_games(self, search_term: str, limit: int = 5) -> List[Dict]:
        """Search for games by title"""
        try:
            all_games = await self.fetch_games_list()
            
            matching_games = [
                game for game in all_games 
                if search_term.lower() in game.get("title", "").lower()
            ]
            
            return matching_games[:limit]
            
        except Exception as e:
            print(f"Error searching games: {e}")
            return []

    async def get_games_by_platform(self, platform: str, limit: int = 10) -> List[Dict]:
        """Get games filtered by platform"""
        try:
            games = await self.fetch_games_list(platform=platform)
            return games[:limit]
        except Exception as e:
            print(f"Error getting games by platform: {e}")
            return []

    async def get_random_games(self, count: int = 1) -> List[Dict]:
        """Get random games"""
        try:
            import random
            all_games = await self.fetch_games_list()
            
            if len(all_games) < count:
                return all_games
            
            return random.sample(all_games, count)
            
        except Exception as e:
            print(f"Error getting random games: {e}")
            return []