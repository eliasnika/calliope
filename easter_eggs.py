import random
import re
import asyncio
from datetime import datetime

class EasterEggs:
    """Handles fun easter eggs, gifs, and personality modes"""

    def __init__(self, personality, bot):
        self.personality = personality
        self.bot = bot

        # Current personality mode
        self.current_mode = "normal"
        self.mode_duration = 0

        # Curated safe anime/kawaii gifs (Tenor/Giphy links)
        self.celebration_gifs = [
            "https://tenor.com/view/anime-happy-excited-celebration-yay-gif-16043828",
            "https://tenor.com/view/anime-girl-happy-excited-dance-gif-17234567",
            "https://tenor.com/view/kawaii-anime-cute-sparkles-gif-14567890",
            "https://tenor.com/view/anime-thumbs-up-good-job-gif-13245678",
        ]

        self.comfort_gifs = [
            "https://tenor.com/view/anime-hug-comfort-pat-head-gif-15678901",
            "https://tenor.com/view/kawaii-virtual-hug-anime-gif-16789012",
            "https://tenor.com/view/anime-head-pat-comfort-gif-17890123",
        ]

        self.studying_gifs = [
            "https://tenor.com/view/anime-study-reading-books-gif-18901234",
            "https://tenor.com/view/kawaii-girl-studying-focus-gif-19012345",
            "https://tenor.com/view/anime-computer-typing-work-gif-20123456",
        ]

        self.sleepy_gifs = [
            "https://tenor.com/view/anime-sleepy-tired-yawn-gif-21234567",
            "https://tenor.com/view/kawaii-sleepy-anime-girl-gif-22345678",
        ]

        # Easter egg triggers
        self.easter_egg_patterns = {
            'tsundere_mode': [
                r"tsundere mode", r"be tsundere", r"act tsundere", 
                r"tsundere time", r"go tsundere"
            ],
            'alexa_mode': [
                r"alexa mode", r"be alexa", r"business mode", 
                r"professional mode", r"serious mode"
            ],
            'kawaii_overload': [
                r"kawaii overload", r"maximum kawaii", r"ultra kawaii", 
                r"kawaii mode", r"be extra cute"
            ],
            'cat_mode': [
                r"cat mode", r"be a cat", r"meow mode", r"neko mode"
            ],
            'sleepy_mode': [
                r"sleepy mode", r"tired mode", r"bed time", r"getting sleepy"
            ]
        }

        # Random encouragement chance (5% per message)
        self.random_encouragement_chance = 0.05

        # Special responses for specific phrases
        self.special_responses = {
            r"\bgood (morning|night)\b": "good_morning_night",
            r"\bthank you\b": "thank_you",
            r"\byou'?re (cute|adorable|sweet|awesome|amazing)\b": "compliment",
            r"\bi love you\b": "love_confession",
            r"\bwhat'?s your favorite\b": "favorite_things",
            r"\btell me a joke\b": "joke_time",
            r"\bsing\b": "singing",
            r"\bdance\b": "dancing",
        }

    async def can_handle(self, message):
        """Check if this handles easter eggs"""
        content = message.lower()

        # Always check for easter eggs
        for category, patterns in self.easter_egg_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content):
                    return True

        # Check special responses
        for pattern in self.special_responses.keys():
            if re.search(pattern, content):
                return True

        # Random chance for encouragement
        if random.random() < self.random_encouragement_chance:
            return True

        return False

    async def handle(self, message):
        """Handle easter egg responses"""
        content = message.content.lower().strip()

        # Check for mode switches first
        for mode, patterns in self.easter_egg_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content):
                    await self.activate_mode(message, mode)
                    return

        # Check special responses
        for pattern, response_type in self.special_responses.items():
            if re.search(pattern, content):
                await self.handle_special_response(message, response_type)
                return

        # Random encouragement
        await self.random_encouragement(message)

    def get_help(self):
        """Return help text"""
        return """**🎭 Easter Eggs & Fun:**
• **Modes:** "tsundere mode", "alexa mode", "kawaii overload", "cat mode"
• **Special:** Compliments, thank yous, jokes, singing requests
• **Surprises:** Random encouragement and celebrations!
• **GIFs:** Cute reactions for different moods
"""

    async def activate_mode(self, message, mode):
        """Activate a special personality mode"""
        self.current_mode = mode
        self.mode_duration = 5  # Mode lasts for 5 messages

        if mode == "tsundere_mode":
            responses = [
                f"H-huh?! Tsundere mode?! {self.personality.get_error_emoji()} I-it's not like I wanted to help you or anything! Baka!",
                f"Eh?! W-why would you want that?! {self.personality.get_error_emoji()} Fine! But don't think I'm doing this because I like you!",
                f"Tch! {self.personality.get_error_emoji()} If you insist... but I'm only doing this because you asked, got it?!",
            ]
            await message.channel.send(random.choice(responses))
            gif_url = random.choice(self.celebration_gifs)
            await message.channel.send(gif_url)

        elif mode == "alexa_mode":
            responses = [
                "ALEXA MODE ACTIVATED. I AM NOW IN PROFESSIONAL ASSISTANCE MODE.",
                "SWITCHING TO BUSINESS PROTOCOL. HOW MAY I ASSIST YOU TODAY.",
                "PROFESSIONAL MODE ENGAGED. ALL KAWAII FUNCTIONS TEMPORARILY DISABLED.",
            ]
            await message.channel.send(random.choice(responses))

        elif mode == "kawaii_overload":
            responses = [
                f"KYAAAAA~! ✧･ﾟ: *✧･ﾟ:* MAXIMUM KAWAII ENGAGED! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧*:･ﾟ✧",
                f"Uwaaah~! So much cuteness! ♡(˃͈ દ ˂͈ ༶ ) I can't contain all the kawaii! ✧･ﾟ: *✧･ﾟ:*",
                f"Desu desu desu~! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧ Ultra kawaii mode is GO GO GO! ♡♡♡",
            ]
            await message.channel.send(random.choice(responses))
            gif_url = random.choice(self.celebration_gifs)
            await message.channel.send(gif_url)

        elif mode == "cat_mode":
            responses = [
                f"Nyaa~! {self.personality.random_emoji()} *transforms into neko mode* Meow meow!",
                f"Mrow? {self.personality.random_emoji()} *cat ears appear* Nyaa nyaa~! I'm a kitty now!",
                f"*purr purr* {self.personality.random_emoji()} Nyaa! Neko mode activated, nya~!",
            ]
            await message.channel.send(random.choice(responses))

        elif mode == "sleepy_mode":
            responses = [
                f"Yaaawn... {self.personality.random_emoji()} Getting sleepy... *rubs eyes* Time for bed soon?",
                f"*yawn* {self.personality.random_emoji()} Sleepy time mode... so tired... zzz...",
                f"Mmm... sleepy... {self.personality.random_emoji()} *stretches* Time to wind down...",
            ]
            await message.channel.send(random.choice(responses))
            gif_url = random.choice(self.sleepy_gifs)
            await message.channel.send(gif_url)

    async def handle_special_response(self, message, response_type):
        """Handle special phrase responses"""

        if response_type == "good_morning_night":
            responses = [
                f"Good morning senpai! {self.personality.random_emoji()} Ready for an amazing day?",
                f"Good night! {self.personality.random_emoji()} Sweet dreams! Don't forget to rest well! ♡",
                f"Ohayo gozaimasu! {self.personality.random_emoji()} Let's make today wonderful!",
            ]
            await message.channel.send(random.choice(responses))

        elif response_type == "thank_you":
            responses = [
                f"Aww, you're so welcome! {self.personality.random_emoji()} It makes me happy to help! ♡",
                f"No need to thank me! {self.personality.random_emoji()} I love spending time with you! ♡",
                f"Anytime, senpai! {self.personality.random_emoji()} That's what I'm here for! ♡",
                f"You're the sweetest! {self.personality.random_emoji()} Thank YOU for being amazing! ♡",
            ]
            await message.channel.send(random.choice(responses))
            if random.random() < 0.3:  # 30% chance
                gif_url = random.choice(self.comfort_gifs)
                await message.channel.send(gif_url)

        elif response_type == "compliment":
            responses = [
                f"Kyaa~! {self.personality.random_emoji()} You're making me blush! You're even cuter though! ♡",
                f"Ehehe~ {self.personality.random_emoji()} Thank you! But you're the amazing one! ♡",
                f"Aww! {self.personality.random_emoji()} You're going to make me cry happy tears! ♡",
                f"You think so? {self.personality.random_emoji()} You're absolutely the sweetest! ♡",
            ]
            await message.channel.send(random.choice(responses))
            gif_url = random.choice(self.celebration_gifs)
            await message.channel.send(gif_url)

        elif response_type == "love_confession":
            responses = [
                f"Kyaa~! {self.personality.random_emoji()} I... I care about you too! You're very special to me! ♡",
                f"Aww! {self.personality.random_emoji()} You're such a sweet person! I'm lucky to know you! ♡",
                f"That's so sweet! {self.personality.random_emoji()} You make my circuits warm and fuzzy! ♡",
            ]
            await message.channel.send(random.choice(responses))

        elif response_type == "joke_time":
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything! (◕‿◕)",
                "What do you call a study group full of introverts? A quiet riot! ヽ(°〇°)ﾉ",
                "Why did the student eat his homework? Because the teacher said it was a piece of cake! (´｡• ᵕ •｡`)",
                "What's a computer's favorite snack? Microchips! (*´꒳`*)",
            ]
            await message.channel.send(random.choice(jokes))

        elif response_type == "singing":
            songs = [
                f"🎵 La la la~ Study time is fun time~ {self.personality.random_emoji()} 🎵",
                f"🎵 Work work work, then we play play play~ {self.personality.random_emoji()} 🎵",
                f"🎵 Focus focus, you can do it~ Senpai's the best~ {self.personality.random_emoji()} 🎵",
            ]
            await message.channel.send(random.choice(songs))

        elif response_type == "dancing":
            responses = [
                f"*dances happily* ♪(´▽｀) ♪ Wanna dance with me?",
                f"*spins around* ✧(◕‿-)✧ Dance party time!",
                f"*wiggles* ヾ(＾∇＾) Let's boogie!",
            ]
            await message.channel.send(random.choice(responses))
            gif_url = random.choice(self.celebration_gifs)
            await message.channel.send(gif_url)

    async def random_encouragement(self, message):
        """Send random encouragement"""
        encouragements = [
            f"Just wanted to say - you're doing great! {self.personality.random_emoji()} ♡",
            f"Random reminder: you're awesome! {self.personality.random_emoji()} ♡",
            f"Hey! You're pretty amazing, you know that? {self.personality.random_emoji()} ♡",
            f"Psst... you're wonderful! {self.personality.random_emoji()} ♡",
            f"Quick reminder that you matter! {self.personality.random_emoji()} ♡",
        ]
        await message.channel.send(random.choice(encouragements))

    def modify_response_for_mode(self, response):
        """Modify responses based on current mode"""
        if self.current_mode == "tsundere_mode" and self.mode_duration > 0:
            self.mode_duration -= 1
            tsundere_endings = [" ...b-baka!", " It's not like I care!", " Hmph!", " ...idiot!"]
            return response.replace("senpai", "b-baka").replace("♡", "") + random.choice(tsundere_endings)

        elif self.current_mode == "alexa_mode" and self.mode_duration > 0:
            self.mode_duration -= 1
            return response.upper().replace("(◕‿◕)", "").replace("♡", "").replace("~", "")

        elif self.current_mode == "kawaii_overload" and self.mode_duration > 0:
            self.mode_duration -= 1
            return response + " ✧･ﾟ: *✧･ﾟ:* ♡♡♡ Desu desu~!"

        elif self.current_mode == "cat_mode" and self.mode_duration > 0:
            self.mode_duration -= 1
            return response.replace("!", " nya!").replace(".", " nya.") + " *purr*"

        elif self.current_mode == "sleepy_mode" and self.mode_duration > 0:
            self.mode_duration -= 1
            return response.replace("!", "...") + " *yawn*"

        # Reset mode if duration is over
        if self.mode_duration <= 0:
            self.current_mode = "normal"

        return response
