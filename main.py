# Import our features
from personality import VTuberPersonality
from pomodoro import PomodoroFeature
from morning import MorningDigest

# Easter egg data
current_mode = "normal"
mode_duration = 0

# Curated safe gifs
celebration_gifs = [
    "https://tenor.com/view/anime-happy-excited-celebration-yay-gif-16043828",
    "https://tenor.com/view/anime-girl-happy-excited-dance-gif-17234567",
    "https://tenor.com/view/kawaii-anime-cute-sparkles-gif-14567890",
]

import discord
from discord.ext import commands
import os
import re
import random
import asyncio

# Import our features
from personality import VTuberPersonality
from pomodoro import PomodoroFeature
from morning import MorningDigest

# Simple easter egg variables
current_mode = "normal"
mode_duration = 0
# from music import MusicFeature  # Future feature!

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True
bot = commands.Bot(command_prefix=None, intents=intents)

# Initialize components
personality = VTuberPersonality()
pomodoro = PomodoroFeature(personality)
morning = MorningDigest(personality, bot)

# Feature registry - super easy to add new ones!
features = {
    'pomodoro': pomodoro,
    'morning': morning,
    # 'music': music,  # Add when ready!
}

@bot.event
async def on_ready():
    print(f'🌟 {bot.user} is ready!')
    print(f'✨ Kawaii study bot activated! (◕‿◕)♡')
    print(f'🌅 Morning digest available on demand!')
    print(f'💝 Care & rant features built-in!')
    print(f'🔧 Available features: {list(features.keys())}')

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author == bot.user:
        return

    # Only DMs
    if not isinstance(message.channel, discord.DMChannel):
        return

    # Check if authorized user
    try:
        authorized_user_id = int(os.environ['AUTHORIZED_USER_ID'])
    except (KeyError, ValueError):
        print("❌ AUTHORIZED_USER_ID secret not set!")
        return

    if message.author.id != authorized_user_id:
        await message.channel.send(personality.unauthorized())
        return

    # Process the message
    await handle_message(message)

async def handle_message(message):
    global current_mode, mode_duration
    content = message.content.lower().strip()

    # Check for greetings
    if re.search(r'\b(hi|hello|hey|hiya|yo|ohayo|konnichiwa)\b', content):
        response = personality.greeting()
        response = modify_response_for_mode(response)
        await message.channel.send(response)
        return

    # Check for help
    if re.search(r'\b(help|commands|what can you do)\b', content):
        await show_help(message)
        return

    # Easter egg triggers
    if re.search(r'\b(tsundere mode|be tsundere)\b', content):
        current_mode = "tsundere"
        mode_duration = 5
        await message.channel.send(f"H-huh?! Tsundere mode?! {personality.get_error_emoji()} I-it's not like I wanted to help you or anything! Baka!")
        return

    if re.search(r'\b(alexa mode|business mode|professional mode)\b', content):
        current_mode = "alexa"
        mode_duration = 5
        await message.channel.send("ALEXA MODE ACTIVATED. I AM NOW IN PROFESSIONAL ASSISTANCE MODE.")
        return

    if re.search(r'\b(kawaii overload|maximum kawaii|ultra kawaii)\b', content):
        current_mode = "kawaii"
        mode_duration = 5
        await message.channel.send(f"KYAAAAA~! ✧･ﾟ: *✧･ﾟ:* MAXIMUM KAWAII ENGAGED! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧*:･ﾟ✧")
        return

    if re.search(r'\b(cat mode|neko mode|meow mode)\b', content):
        current_mode = "cat"
        mode_duration = 5
        await message.channel.send(f"Nyaa~! {personality.random_emoji()} *transforms into neko mode* Meow meow!")
        return

    # Special compliment responses
    if re.search(r'\byou\'?re (cute|adorable|sweet|awesome|amazing)\b', content):
        responses = [
            f"Kyaa~! {personality.random_emoji()} You're making me blush! You're even cuter though! ♡",
            f"Ehehe~ {personality.random_emoji()} Thank you! But you're the amazing one! ♡",
            f"Aww! {personality.random_emoji()} You're going to make me cry happy tears! ♡",
        ]
        response = modify_response_for_mode(random.choice(responses))
        await message.channel.send(response)
        # Send a cute celebration gif!
        celebration_gifs = [
            "https://tenor.com/view/giggling-kicking-feet-sped-up-asagao-to-kase-san-yuri-gif-7086509730415310709",
            "https://tenor.com/view/anime-fuck-yeah-yes-yass-gif-5881788"
        ]
        await message.channel.send(random.choice(celebration_gifs))
        return

    # Thank you responses
    if re.search(r'\bthank you\b', content):
        responses = [
            f"Aww, you're so welcome! {personality.random_emoji()} It makes me happy to help! ♡",
            f"No need to thank me! {personality.random_emoji()} I love spending time with you! ♡",
            f"Anytime, senpai! {personality.random_emoji()} That's what I'm here for! ♡",
        ]
        response = modify_response_for_mode(random.choice(responses))
        await message.channel.send(response)
        return

    # Joke requests
    if re.search(r'\btell me a joke\b', content):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything! (◕‿◕)",
            "What do you call a study group full of introverts? A quiet riot! ヽ(°〇°)ﾉ",
            "Why did the student eat his homework? Because the teacher said it was a piece of cake! (´｡• ᵕ •｡`)",
            "What's a computer's favorite snack? Microchips! (*´꒳`*)",
        ]
        response = modify_response_for_mode(random.choice(jokes))
        await message.channel.send(response)
        return

    # Check for rant zone FIRST
    if re.search(r'\b(rant zone|need to rant|let me rant|i need to vent|need to vent)\b', content):
        await handle_rant_zone(message)
        return

    # Check for care/comfort requests
    care_patterns = [
        r"i'?m (sad|depressed|down|upset|hurt|lonely|anxious|stressed)",
        r"feeling (sad|down|upset|hurt|lonely|anxious|stressed|overwhelmed)",
        r"i feel (sad|down|upset|hurt|lonely|anxious|stressed|terrible|awful|bad)",
        r"comfort me",
        r"i need comfort",
        r"hug me",
        r"having a (bad|rough|hard|tough) (day|time)",
    ]

    for pattern in care_patterns:
        if re.search(pattern, content):
            await handle_comfort(message)
            return

    # Check each feature
    for feature_name, feature in features.items():
        print(f"🔍 Checking if {feature_name} can handle: '{content}'")
        if await feature.can_handle(content):
            print(f"✅ {feature_name} will handle this message")
            await feature.handle(message)
            return
        else:
            print(f"❌ {feature_name} cannot handle this")

    print(f"📝 No feature could handle '{content}', using casual response")
    # Default casual response with mode modification
    response = personality.casual_response()
    response = modify_response_for_mode(response)

    # 5% chance for random encouragement
    if random.random() < 0.05:
        encouragements = [
            f"Just wanted to say - you're doing great! {personality.random_emoji()} ♡",
            f"Random reminder: you're awesome! {personality.random_emoji()} ♡",
            f"Hey! You're pretty amazing, you know that? {personality.random_emoji()} ♡",
        ]
        response = modify_response_for_mode(random.choice(encouragements))

    await message.channel.send(response)

def modify_response_for_mode(response):
    """Modify responses based on current personality mode"""
    global current_mode, mode_duration

    if current_mode == "tsundere" and mode_duration > 0:
        mode_duration -= 1
        tsundere_endings = [" ...b-baka!", " It's not like I care!", " Hmph!", " ...idiot!"]
        return response.replace("senpai", "b-baka").replace("♡", "") + random.choice(tsundere_endings)

    elif current_mode == "alexa" and mode_duration > 0:
        mode_duration -= 1
        return response.upper().replace("(◕‿◕)", "").replace("♡", "").replace("~", "").replace("!", ".")

    elif current_mode == "kawaii" and mode_duration > 0:
        mode_duration -= 1
        return response + " ✧･ﾟ: *✧･ﾟ:* ♡♡♡ Desu desu~!"

    elif current_mode == "cat" and mode_duration > 0:
        mode_duration -= 1
        return response.replace("!", " nya!").replace(".", " nya.") + " *purr*"

    # Reset mode if duration is over
    if mode_duration <= 0:
        current_mode = "normal"

    return response

async def handle_rant_zone(message):
    """Handle rant zone activation"""
    rant_openings = [
        f"RANT ZONE ACTIVATED! {personality.random_emoji()} I'm here to listen. Let it ALL out! 🗣️",
        f"Yes! Vent away, senpai! {personality.random_emoji()} I've got time and I'm not judging. 💬",
        f"Rant mode: ON! {personality.random_emoji()} Say whatever you need to say. I'm listening! 👂",
        f"Let it out! {personality.random_emoji()} Sometimes you just need someone to hear you. I'm here! 🎯",
        f"VENT AWAY! {personality.random_emoji()} No judgment, just ears. Tell me everything! 💭",
    ]

    await message.channel.send(random.choice(rant_openings))
    await asyncio.sleep(1)

    encouragements = [
        f"What's got you fired up? I'm ready to listen to every word. {personality.random_emoji()}",
        f"Spill it all! Don't hold back - this is your space to be real. {personality.random_emoji()}",
        f"Tell me what's been building up inside. I want to hear it all! {personality.random_emoji()}",
        f"What's eating at you? I'm ready for the full story, no limits! {personality.random_emoji()}",
    ]

    await message.channel.send(random.choice(encouragements))

async def handle_comfort(message):
    """Handle comfort requests"""
    comfort_responses = [
        f"Oh sweetie... {personality.get_error_emoji()} I'm here for you. You're not alone. ♡",
        f"Aww, senpai... {personality.get_error_emoji()} *virtual hug* I care about you so much. ♡",
        f"I'm so sorry you're going through this. {personality.get_error_emoji()} You're brave for reaching out. ♡",
        f"*gentle hug* {personality.get_error_emoji()} Whatever you're feeling is valid. I'm here. ♡",
        f"Sweet senpai... {personality.get_error_emoji()} You don't have to face this alone. I believe in you. ♡",
    ]

    await message.channel.send(random.choice(comfort_responses))
    await asyncio.sleep(2)

    follow_ups = [
        f"Take a deep breath with me... breathe in... and out... {personality.random_emoji()} You're stronger than you know.",
        f"Remember: this feeling will pass. You've gotten through hard times before. {personality.random_emoji()}",
        f"You're doing better than you think you are. Sometimes we're our own harshest critics. {personality.random_emoji()}",
        f"It's okay to rest. It's okay to take things one moment at a time. {personality.random_emoji()}",
    ]

    await message.channel.send(random.choice(follow_ups))

async def show_help(message):
    help_text = f"""
🌟 **Hiya! I'm your kawaii study buddy!** {personality.random_emoji()}

**✨ What I can do:**
"""

    # Add help for each feature
    for feature_name, feature in features.items():
        help_text += f"\n{feature.get_help()}"

    help_text += f"""

**💡 Tips:**
• Just talk naturally! I understand lots of ways to say things~
• I'll cheer you on and keep you motivated! {personality.random_emoji()}

Ready to be productive together? {personality.random_emoji()}
    """

    await message.channel.send(help_text)

# Run the bot
if __name__ == "__main__":
    try:
        token = os.environ['DISCORD_BOT_TOKEN']
        print("🚀 Starting bot...")
        bot.run(token)
    except KeyError:
        print("❌ DISCORD_BOT_TOKEN secret not set!")
        print("🔧 Add your bot token to Replit secrets!")
