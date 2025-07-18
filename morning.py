import asyncio
import re
import random
from datetime import datetime, timedelta
import aiohttp

class MorningDigest:
    """Manual morning digest with weather, news, and stocks"""

    def __init__(self, personality, bot):
        self.personality = personality
        self.bot = bot

        # Configuration - edit these to customize!
        self.config = {
            "location": "Santa Rosa,CA,US",       # Try this format first!

            # Weather settings
            "weather_units": "imperial",        # imperial = Fahrenheit, metric = Celsius
            "rain_threshold": 30,              # % chance of rain to recommend umbrella
            "cold_threshold": 50,              # Temperature to recommend jacket (F)

            # News sources and topics
            "news_sources": [
                "techcrunch",
                "ars-technica", 
                "hacker-news",
                "the-verge"
            ],
            "news_topics": [
                "technology",
                "programming", 
                "artificial intelligence",
                "startups",
                "science"
            ],
            "max_news_articles": 5,

            # Stock tracking
            "stocks": [
                "AAPL",    # Apple
                "GOOGL",   # Google
                "MSFT",    # Microsoft
                "TSLA",    # Tesla
                "NVDA",    # Nvidia
                # Add your favorite stocks here!
            ],
            "stock_change_threshold": 2.0,     # Only show if change > 2%
        }

        # Manual trigger patterns
        self.morning_patterns = [
            r"morning digest",
            r"morning routine",
            r"daily briefing",
            r"wake up",
            r"good morning",
            r"morning update",
            r"start my day",
            r"daily summary",
            r"morning brief",
        ]

    async def can_handle(self, message):
        """Check if this feature can handle the message"""
        keywords = [
            'morning', 'digest', 'routine', 'briefing', 'weather', 
            'news', 'stocks', 'wake', 'daily', 'update', 'summary'
        ]

        return any(keyword in message.lower() for keyword in keywords)

    async def handle(self, message):
        """Handle morning digest related messages"""
        content = message.content.lower().strip()

        # Check for full morning digest
        for pattern in self.morning_patterns:
            if re.search(pattern, content):
                await self.send_morning_digest(message)
                return

        # Check for individual components
        if any(word in content for word in ['weather', 'temperature', 'rain', 'forecast']):
            await self.send_weather_update(message)
            return

        if any(word in content for word in ['news', 'headlines', 'articles']):
            await self.send_news_update(message)
            return

        if any(word in content for word in ['stocks', 'market', 'shares', 'portfolio']):
            await self.send_stock_update(message)
            return

        # Default help response
        await self.send_help_message(message)

    def get_help(self):
        """Return help text for this feature"""
        return """**🌅 Morning Digest:**
• **Full digest:** "morning digest", "daily briefing", "good morning"
• **Weather only:** "weather update", "forecast"
• **News only:** "tech news", "daily headlines" 
• **Stocks only:** "stock update", "market check"
"""

    async def send_morning_digest(self, message):
        """Send the full morning digest"""
        # Morning greeting
        greetings = [
            f"Good morning senpai! {self.personality.random_emoji()} Here's your daily briefing~",
            f"Ohayo! {self.personality.random_emoji()} Ready for today's digest?",
            f"Morning briefing time! {self.personality.random_emoji()} Let's see what's happening~",
            f"Daily update ready! {self.personality.random_emoji()} Time to start your day informed!",
        ]
        greeting = random.choice(greetings)

        await message.channel.send(greeting)
        await asyncio.sleep(1)

        # Send each section
        try:
            await self.send_weather_update(message)
            await asyncio.sleep(2)
            await self.send_news_update(message) 
            await asyncio.sleep(2)
            await self.send_stock_update(message)

            # Encouraging wrap-up
            wrap_ups = [
                f"Have an amazing day! {self.personality.random_emoji()} You've got this!",
                f"Ready to conquer the day? {self.personality.random_emoji()} Let's gooo!",
                f"All set for today! {self.personality.random_emoji()} Make it count!",
                f"Stay awesome! {self.personality.random_emoji()} Today's gonna be great!",
            ]
            await asyncio.sleep(1)
            await message.channel.send(random.choice(wrap_ups))

        except Exception as e:
            await message.channel.send(f"Oops! {self.personality.random_emoji()} Had trouble getting some info, but you're still awesome!")
            print(f"❌ Morning digest error: {e}")

    async def send_weather_update(self, message):
        """Send weather information"""
        loading_msg = await message.channel.send(f"Getting weather data... {self.personality.random_emoji()}")

        try:
            weather_data = await self.get_weather_data()
            if not weather_data:
                await message.channel.send(f"Couldn't get weather data! {self.personality.get_error_emoji()} Check the console for error details.")
                return

            # Extract weather info
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            description = weather_data['weather'][0]['description'].title()
            humidity = weather_data['main']['humidity']

            # Get appropriate emoji for temperature
            weather_emoji = self.personality.get_weather_emoji(temp)

            # Check for rain
            rain_chance = 0
            if 'rain' in weather_data:
                rain_chance = weather_data['rain'].get('1h', 0) * 10  # Convert mm to rough %
            elif any('rain' in w['description'].lower() for w in weather_data.get('weather', [])):
                rain_chance = 60  # If rain is mentioned, assume significant chance

            # Build weather message with better formatting
            weather_msg = f"🌤️ **Weather in {self.config['location']}**\n"
            weather_msg += f"• **{temp:.0f}°F** (feels like {feels_like:.0f}°F)\n"
            weather_msg += f"• **{description}**\n"
            weather_msg += f"• **Humidity:** {humidity}%"

            # Recommendations
            recommendations = []
            if rain_chance > self.config['rain_threshold']:
                recommendations.append(f"☔ Bring an umbrella! ~{rain_chance:.0f}% chance of rain")

            if temp < self.config['cold_threshold']:
                recommendations.append(f"🧥 Grab a jacket! It's chilly today")

            if temp > 80:
                recommendations.append(f"🌞 Perfect weather! Maybe shorts today?")

            if recommendations:
                weather_msg += f"\n\n**Recommendations:**\n" + "\n".join(f"• {rec}" for rec in recommendations)

            weather_msg += f"\n\nHave a great day out there! {weather_emoji}"

            await message.channel.send(weather_msg)

        except Exception as e:
            await message.channel.send(f"Weather check failed! {self.personality.get_error_emoji()} But every day is a good day with you!")
            print(f"❌ Weather error: {e}")

    async def send_news_update(self, message):
        """Send personalized news digest"""
        loading_msg = await message.channel.send(f"Fetching latest news... {self.personality.random_emoji()}")

        try:
            news_data = await self.get_news_data()
            if not news_data:
                await message.channel.send(f"Couldn't get news today! {self.personality.get_error_emoji()} Check the console for error details.")
                return

            # Send header
            await message.channel.send(f"📰 **Your Daily Tech Digest** {self.personality.random_emoji()}")

            # Send each article as its own message for clean preview layout
            for i, article in enumerate(news_data[:self.config['max_news_articles']], 1):
                title = article.get('title', 'No title')
                source = article.get('source', {}).get('name', 'Unknown')
                url = article.get('url', '')

                # Truncate long titles
                if len(title) > 100:
                    title = title[:97] + "..."

                # Create individual message for each article
                article_msg = f"**{i}.** {title}\n"
                article_msg += f"*Source: {source}*"

                if url:
                    article_msg += f"\n{url}"

                await message.channel.send(article_msg)

                # Small delay between articles for readability
                await asyncio.sleep(0.5)

            # Send footer
            await message.channel.send(f"Stay informed! {self.personality.random_emoji()}")

        except Exception as e:
            await message.channel.send(f"News update failed! {self.personality.get_error_emoji()} But you're always my top story!")
            print(f"❌ News error: {e}")

    async def send_stock_update(self, message):
        """Send stock market update"""
        loading_msg = await message.channel.send(f"Checking your portfolio... {self.personality.random_emoji()}")

        try:
            stock_data = await self.get_stock_data()
            if not stock_data:
                await message.channel.send(f"Couldn't get stock data! {self.personality.get_error_emoji()} Check the console for error details.")
                return

            stock_msg = f"📈 **Your Portfolio Check** {self.personality.random_emoji()}\n\n"

            for symbol, data in stock_data.items():
                price = data.get('price', 0)
                change = data.get('change', 0)
                change_pct = data.get('change_percent', 0)

                # Only show if significant change
                if abs(change_pct) >= self.config['stock_change_threshold']:
                    emoji = "📈" if change > 0 else "📉"
                    stock_msg += f"{emoji} **{symbol}**: ${price:.2f} "
                    stock_msg += f"({change:+.2f}, {change_pct:+.1f}%)\n"

            if stock_msg == f"📈 **Your Portfolio Check** {self.personality.random_emoji()}\n\n":
                stock_msg += f"All stocks stable today! {self.personality.random_emoji()} Steady as you go!"
            else:
                stock_msg += f"\n*Only showing changes > {self.config['stock_change_threshold']}%*"

            stock_msg += f"\n\nKeep investing in yourself! {self.personality.random_emoji()}"

            await message.channel.send(stock_msg)

        except Exception as e:
            await message.channel.send(f"Stock check failed! {self.personality.get_error_emoji()} But you're always a valuable investment!")
            print(f"❌ Stock error: {e}")

    async def send_help_message(self, message):
        """Send help for morning digest"""
        help_msg = f"""
🌅 **Morning Digest Help** {self.personality.random_emoji()}

**What I can do:**
• **Full digest:** "morning digest", "daily briefing", "good morning"
• **Weather:** "weather update" for {self.config['location']}
• **News:** "tech news" from your favorite sources
• **Stocks:** "stock update" for your portfolio

**Current settings:**
• **Location:** {self.config['location']}
• **Tracking:** {len(self.config['stocks'])} stocks
• **News sources:** {len(self.config['news_sources'])} sources

Want to customize? Edit the config in morning.py! {self.personality.random_emoji()}
        """

        await message.channel.send(help_msg)

    # API Methods - Real implementations!
    async def get_weather_data(self):
        """Get weather data from OpenWeatherMap API"""
        import os

        api_key = os.environ.get('OPENWEATHER_API_KEY')
        if not api_key:
            print("❌ OPENWEATHER_API_KEY not set in secrets!")
            return None

        print(f"🌤️ Using weather API key: {api_key[:8]}...")

        try:
            # Try multiple location formats for better success
            location_formats = [
                self.config['location'],                    # Original format
                self.config['location'].replace(', ', ','), # Remove spaces
                self.config['location'].replace(',CA,US', ',California,US'), # Full state name
                'Santa Rosa,California,US',                 # Explicit format
                'Santa Rosa,CA',                           # Simple format
                'Santa Rosa'                               # Just city name
            ]

            geo_data = None
            successful_location = None

            async with aiohttp.ClientSession() as session:
                # Try each location format until one works
                for location_attempt in location_formats:
                    print(f"🗺️ Trying location format: {location_attempt}")

                    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
                    geo_params = {
                        'q': location_attempt,
                        'limit': 1,
                        'appid': api_key
                    }

                    async with session.get(geocoding_url, params=geo_params) as geo_response:
                        if geo_response.status == 200:
                            temp_geo_data = await geo_response.json()
                            if temp_geo_data:
                                geo_data = temp_geo_data
                                successful_location = location_attempt
                                print(f"✅ Found location with format: {location_attempt}")
                                break
                        else:
                            print(f"❌ Failed for {location_attempt}: {geo_response.status}")

                if not geo_data:
                    print(f"❌ Could not find location with any format!")
                    return None

                lat, lon = geo_data[0]['lat'], geo_data[0]['lon']
                location_name = geo_data[0].get('name', 'Unknown')
                print(f"📍 Found: {location_name} at coordinates: {lat}, {lon}")

                # Get weather data
                weather_url = "https://api.openweathermap.org/data/2.5/weather"
                weather_params = {
                    'lat': lat,
                    'lon': lon,
                    'appid': api_key,
                    'units': self.config['weather_units']
                }

                print(f"🌤️ Getting weather data...")

                async with session.get(weather_url, params=weather_params) as weather_response:
                    print(f"🌤️ Weather response status: {weather_response.status}")

                    if weather_response.status != 200:
                        error_text = await weather_response.text()
                        print(f"❌ Weather API failed: {weather_response.status} - {error_text}")
                        return None

                    weather_data = await weather_response.json()
                    print(f"✅ Weather data received successfully!")
                    return weather_data

        except Exception as e:
            print(f"❌ Weather API error: {e}")
            return None

    async def get_news_data(self):
        """Get news from NewsAPI"""
        import os

        api_key = os.environ.get('NEWS_API_KEY')
        if not api_key:
            print("❌ NEWS_API_KEY not set in secrets!")
            return None

        print(f"📰 Using news API key: {api_key[:8]}...")

        try:
            async with aiohttp.ClientSession() as session:
                # Try a simpler query first - just get recent tech articles
                news_url = "https://newsapi.org/v2/everything"

                # Try multiple query strategies
                query_attempts = [
                    # Strategy 1: Just sources, no topic filter, last 7 days
                    {
                        'apiKey': api_key,
                        'sources': ','.join(self.config['news_sources']),
                        'sortBy': 'publishedAt',
                        'language': 'en',
                        'pageSize': 20,
                        'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                    },
                    # Strategy 2: Just topic, no source filter
                    {
                        'apiKey': api_key,
                        'q': 'technology',
                        'sortBy': 'publishedAt',
                        'language': 'en',
                        'pageSize': 20,
                        'from': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
                    },
                    # Strategy 3: Very broad search
                    {
                        'apiKey': api_key,
                        'q': 'tech',
                        'sortBy': 'publishedAt',
                        'language': 'en',
                        'pageSize': 20,
                        'from': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                    }
                ]

                for i, params in enumerate(query_attempts):
                    print(f"📰 Trying query strategy {i+1}...")
                    print(f"📰 Params: {params}")

                    async with session.get(news_url, params=params) as response:
                        print(f"📰 Strategy {i+1} response status: {response.status}")

                        if response.status != 200:
                            error_text = await response.text()
                            print(f"❌ Strategy {i+1} failed: {response.status} - {error_text}")
                            continue

                        data = await response.json()
                        articles = data.get('articles', [])
                        print(f"📰 Strategy {i+1} found {len(articles)} articles")

                        if articles:
                            # Found articles! Process them
                            good_articles = []
                            for j, article in enumerate(articles):
                                title = article.get('title', 'No title')
                                url = article.get('url', '')

                                if (article.get('title') and 
                                    article.get('url') and 
                                    article.get('title') != '[Removed]' and
                                    len(good_articles) < self.config['max_news_articles']):
                                    good_articles.append(article)
                                    print(f"✅ Added: {title[:50]}...")

                            print(f"✅ Strategy {i+1} success! Returning {len(good_articles)} articles")
                            return good_articles
                        else:
                            print(f"❌ Strategy {i+1} returned 0 articles")

                print(f"❌ All strategies failed to find articles")
                return None

        except Exception as e:
            print(f"❌ News API error: {e}")
            return None

    async def get_stock_data(self):
        """Get stock data from Alpha Vantage API"""
        import os

        api_key = os.environ.get('STOCK_API_KEY')
        if not api_key:
            print("❌ STOCK_API_KEY not set!")
            return None

        try:
            stock_results = {}

            async with aiohttp.ClientSession() as session:
                for symbol in self.config['stocks']:
                    # Get quote data for each stock
                    stock_url = "https://www.alphavantage.co/query"
                    params = {
                        'function': 'GLOBAL_QUOTE',
                        'symbol': symbol,
                        'apikey': api_key
                    }

                    async with session.get(stock_url, params=params) as response:
                        if response.status != 200:
                            print(f"❌ Stock API failed for {symbol}: {response.status}")
                            continue

                        data = await response.json()
                        quote = data.get('Global Quote', {})

                        if not quote:
                            print(f"❌ No stock data for {symbol}")
                            continue

                        # Extract relevant data
                        try:
                            price = float(quote.get('05. price', 0))
                            change = float(quote.get('09. change', 0))
                            change_percent = float(quote.get('10. change percent', '0%').replace('%', ''))

                            stock_results[symbol] = {
                                'price': price,
                                'change': change,
                                'change_percent': change_percent
                            }
                        except (ValueError, KeyError) as e:
                            print(f"❌ Error parsing stock data for {symbol}: {e}")
                            continue

                    # Be nice to the API - small delay between requests
                    await asyncio.sleep(0.2)

            return stock_results if stock_results else None

        except Exception as e:
            print(f"❌ Stock API error: {e}")
            return None
