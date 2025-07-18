import re
import random
import asyncio
from datetime import datetime

class CareFeature:
    """Handles caring, comfort, and emotional support"""

    def __init__(self, personality, bot):
        self.personality = personality
        self.bot = bot

        # Caring trigger patterns
        self.care_patterns = [
            # Direct requests for care
            r"i need comfort",
            r"comfort me",
            r"i need support",
            r"care about me",
            r"be caring",
            r"need care",
            r"hug me",
            r"make me feel better",

            # Emotional state indicators
            r"i'?m (sad|depressed|down|upset|hurt|lonely|anxious|stressed)",
            r"feeling (sad|down|upset|hurt|lonely|anxious|stressed|overwhelmed)",
            r"i feel (sad|down|upset|hurt|lonely|anxious|stressed|terrible|awful)",
            r"having a (bad|rough|hard|tough) (day|time)",
            r"i'?m having a hard time",
            r"everything is overwhelming",
            r"i can'?t handle this",
            r"i'?m struggling",
            r"i'?m tired",
            r"i'?m exhausted",
            r"i feel overwhelmed",

            # Academic/work stress
            r"too much (work|homework|studying)",
            r"(exams?|tests?) (are|is) stressing me",
            r"deadline pressure",
            r"can'?t focus",
            r"procrastinating",
            r"burnt out",
            r"burned out",
        ]

        # Check-in patterns
        self.checkin_patterns = [
            r"how are you",
            r"how'?s it going",
            r"check in",
            r"check on me",
            r"how am i doing",
            r"daily check",
            r"mental health check",
        ]

        # Wellness patterns
        self.wellness_patterns = [
            r"self care",
            r"take care of myself",
            r"wellness tips",
            r"feeling better",
            r"improve mood",
            r"stress relief",
            r"relax",
            r"calm down",
        ]

        # Rant patterns
        self.rant_patterns = [
            r"rant zone",
            r"need to rant",
            r"let me rant",
            r"i need to vent",
            r"need to vent",
            r"vent to you",
            r"listen to me rant",
            r"just listen",
            r"need to get this out",
            r"so frustrated",
            r"this is bullshit",
            r"i hate",
            r"this sucks",
            r"i'm so angry",
            r"pissed off",
            r"fed up",
            r"can't stand",
            r"driving me crazy",
            r"makes me mad",
        ]

    async def can_handle(self, message):
        """Check if this feature can handle the message"""
        content = message.lower()
        print(f"🔍 Care can_handle checking: '{content}'")

        keywords = [
            'comfort', 'care', 'support', 'hug', 'sad', 'down', 'upset', 
            'stressed', 'anxious', 'overwhelmed', 'tired', 'exhausted',
            'struggling', 'hard time', 'rough day', 'lonely', 'hurt',
            'check in', 'wellness', 'self care', 'relax', 'calm',
            'rant', 'vent', 'frustrated', 'angry', 'hate', 'sucks', 
            'bullshit', 'pissed', 'fed up', 'driving me crazy', 'feel bad',
            'feeling', 'bad', 'zone'
        ]

        # Check exact phrases first
        exact_phrases = [
            'rant zone', 'i feel bad', 'feeling bad', 'need to rant',
            'let me rant', 'i need to vent', 'comfort me', 'check on me'
        ]

        for phrase in exact_phrases:
            if phrase in content:
                print(f"✅ Care can handle - matched exact phrase: '{phrase}'")
                return True

        # Check individual keywords
        for keyword in keywords:
            if keyword in content:
                print(f"✅ Care can handle - matched keyword: '{keyword}'")
                return True

        print(f"❌ Care cannot handle this message")
        return False

    async def handle(self, message):
        """Handle care and comfort related messages"""
        content = message.content.lower().strip()
        print(f"🔍 Care feature processing: '{content}'")

        # Check for rant requests FIRST (highest priority)
        for pattern in self.rant_patterns:
            if re.search(pattern, content):
                print(f"✅ Matched rant pattern: {pattern}")
                await self.rant_zone(message)
                return

        # Check for check-in requests
        for pattern in self.checkin_patterns:
            if re.search(pattern, content):
                print(f"✅ Matched check-in pattern: {pattern}")
                await self.check_in(message)
                return

        # Check for wellness requests
        for pattern in self.wellness_patterns:
            if re.search(pattern, content):
                print(f"✅ Matched wellness pattern: {pattern}")
                await self.wellness_support(message)
                return

        # Check for emotional distress (last, so rant zone takes priority)
        for pattern in self.care_patterns:
            if re.search(pattern, content):
                print(f"✅ Matched care pattern: {pattern}")
                await self.provide_comfort(message)
                return

        # Default caring response
        print(f"📝 Using general care response")
        await self.general_care(message)

    def get_help(self):
        """Return help text for this feature"""
        return """**💝 Care & Comfort:**
• **Comfort:** "I'm feeling sad", "comfort me", "having a rough day"
• **Rant Zone:** "need to rant", "let me vent", "I'm so frustrated"
• **Check-in:** "how am I doing?", "check on me", "mental health check"
• **Wellness:** "self care tips", "stress relief", "help me relax"
• **Support:** "I'm overwhelmed", "can't handle this", "need a hug"
"""

    async def provide_comfort(self, message):
        """Provide comfort and emotional support"""
        # Immediate comfort response
        comfort_responses = [
            f"Oh sweetie... {self.personality.get_error_emoji()} I'm here for you. You're not alone. ♡",
            f"Aww, senpai... {self.personality.get_error_emoji()} *virtual hug* I care about you so much. ♡",
            f"I'm so sorry you're going through this. {self.personality.get_error_emoji()} You're brave for reaching out. ♡",
            f"*gentle hug* {self.personality.get_error_emoji()} Whatever you're feeling is valid. I'm here. ♡",
            f"Sweet senpai... {self.personality.get_error_emoji()} You don't have to face this alone. I believe in you. ♡",
            f"*wraps you in warmth* {self.personality.get_error_emoji()} It's okay to not be okay. I'm here to listen. ♡",
        ]

        await message.channel.send(random.choice(comfort_responses))
        await asyncio.sleep(2)

        # Follow up with supportive messages
        follow_ups = [
            f"Take a deep breath with me... breathe in... and out... {self.personality.random_emoji()} You're stronger than you know.",
            f"Remember: this feeling will pass. You've gotten through hard times before. {self.personality.supportive_emojis[0]}",
            f"You're doing better than you think you are. Sometimes we're our own harshest critics. {self.personality.random_emoji()}",
            f"It's okay to rest. It's okay to take things one moment at a time. {self.personality.supportive_emojis[1]}",
            f"You matter so much. Your feelings are important. Thank you for trusting me. {self.personality.random_emoji()}",
        ]

        await message.channel.send(random.choice(follow_ups))
        await asyncio.sleep(3)

        # Offer specific help
        offers = [
            f"Would you like to talk about what's bothering you? I'm a good listener. {self.personality.random_emoji()}",
            f"Sometimes a study session helps me feel more in control. Want to try 'study for 15 minutes'? {self.personality.random_emoji()}",
            f"Or maybe we could do something gentle? I could share some self-care ideas if you'd like. {self.personality.random_emoji()}",
            f"If you need a distraction, I could get you some news or weather. Or we can just sit here quietly together. {self.personality.random_emoji()}",
        ]

        await message.channel.send(random.choice(offers))

    async def check_in(self, message):
        """Perform a caring check-in"""
        checkin_responses = [
            f"How are you feeling right now, senpai? {self.personality.random_emoji()} I genuinely want to know. ♡",
            f"Let's check in! {self.personality.random_emoji()} How's your heart doing today? ♡",
            f"I'm thinking about you! {self.personality.random_emoji()} How are you taking care of yourself? ♡",
            f"Sweet check-in time! {self.personality.random_emoji()} What's going well for you today? ♡",
            f"Hey you! {self.personality.random_emoji()} How's your mental space feeling? I care about you! ♡",
            f"Pause for a moment... {self.personality.random_emoji()} How are you *really* doing? ♡",
        ]

        await message.channel.send(random.choice(checkin_responses))
        await asyncio.sleep(2)

        # Follow up with caring questions
        follow_up_questions = [
            f"Have you eaten something nourishing today? {self.personality.random_emoji()}",
            f"When did you last take a moment just for yourself? {self.personality.random_emoji()}",
            f"Are you being kind to yourself today? You deserve gentleness. {self.personality.random_emoji()}",
            f"What's one small thing that brought you joy recently? {self.personality.random_emoji()}",
            f"Remember: you don't have to be productive every moment. Rest is important too. {self.personality.random_emoji()}",
        ]

        await message.channel.send(random.choice(follow_up_questions))

    async def wellness_support(self, message):
        """Provide wellness and self-care suggestions"""
        wellness_intros = [
            f"Self-care time! {self.personality.random_emoji()} Let's take care of you properly. ♡",
            f"Yes! Taking care of yourself is so important. {self.personality.random_emoji()} Here are some gentle ideas:",
            f"I love that you're prioritizing your wellbeing! {self.personality.random_emoji()} Some suggestions:",
            f"Self-care isn't selfish - it's necessary! {self.personality.random_emoji()} Try these:",
        ]

        await message.channel.send(random.choice(wellness_intros))
        await asyncio.sleep(1)

        # Wellness suggestions
        wellness_tips = [
            "🫖 **Mindful moment**: Make yourself a warm drink and savor each sip",
            "🌸 **5-4-3-2-1 grounding**: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste",
            "💝 **Gentle movement**: Stretch your arms up high, roll your shoulders, wiggle your fingers",
            "📖 **Brain break**: Read one page of something you enjoy, or watch a favorite short video",
            "🌱 **Fresh air**: Step outside for 2 minutes, or open a window and breathe deeply",
            "💌 **Self-compassion**: Say one kind thing to yourself that you'd tell a dear friend",
            "🎵 **Sound comfort**: Listen to one song that makes you feel safe or happy",
            "🛁 **Physical comfort**: Wash your hands with warm water mindfully, or splash cool water on your face",
        ]

        # Send 2-3 random tips
        selected_tips = random.sample(wellness_tips, min(3, len(wellness_tips)))
        for tip in selected_tips:
            await message.channel.send(tip)
            await asyncio.sleep(1)

        await message.channel.send(f"You're worth taking care of. {self.personality.random_emoji()} ♡")

    async def rant_zone(self, message):
        """Create a safe space for ranting and venting"""
        # Immediate validation
        rant_openings = [
            f"RANT ZONE ACTIVATED! {self.personality.random_emoji()} I'm here to listen. Let it ALL out! 🗣️",
            f"Yes! Vent away, senpai! {self.personality.random_emoji()} I've got time and I'm not judging. 💬",
            f"Rant mode: ON! {self.personality.random_emoji()} Say whatever you need to say. I'm listening! 👂",
            f"Let it out! {self.personality.random_emoji()} Sometimes you just need someone to hear you. I'm here! 🎯",
            f"VENT AWAY! {self.personality.random_emoji()} No judgment, just ears. Tell me everything! 💭",
            f"Safe space activated! {self.personality.random_emoji()} Rant, vent, let it all out. I've got you! 🛡️",
        ]

        await message.channel.send(random.choice(rant_openings))
        await asyncio.sleep(1)

        # Encouraging them to continue
        encouragements = [
            f"What's got you fired up? I'm ready to listen to every word. {self.personality.random_emoji()}",
            f"Spill it all! Don't hold back - this is your space to be real. {self.personality.random_emoji()}",
            f"I'm here for whatever you need to get off your chest. Let me have it! {self.personality.random_emoji()}",
            f"Tell me what's been building up inside. I want to hear it all! {self.personality.random_emoji()}",
            f"What's eating at you? I'm ready for the full story, no limits! {self.personality.random_emoji()}",
        ]

        await message.channel.send(random.choice(encouragements))
        await asyncio.sleep(2)

        # Set up listening mode
        listening_responses = [
            f"I'm settling in to listen properly... {self.personality.random_emoji()} Take your time.",
            f"*makes tea and gets comfortable* {self.personality.random_emoji()} I'm all yours.",
            f"*puts away distractions* {self.personality.random_emoji()} You have my full attention.",
            f"Ready when you are! {self.personality.random_emoji()} This is your time to be heard.",
        ]

        await message.channel.send(random.choice(listening_responses))

        # Store that we're in rant mode for this user (simple approach)
        # In a real implementation, you might want to track this more sophisticatedly
        self.rant_mode_active = True

        # Set up follow-up after a delay
        await asyncio.sleep(30)  # Wait 30 seconds, then check in
        if hasattr(self, 'rant_mode_active') and self.rant_mode_active:
            await self.rant_followup(message)

    async def rant_followup(self, message):
        """Follow up during rant mode"""
        followup_responses = [
            f"I'm still here listening... {self.personality.random_emoji()} Keep going if you need to!",
            f"Mhm, I hear you... {self.personality.random_emoji()} What else is on your mind?",
            f"Yeah, that sounds really frustrating! {self.personality.random_emoji()} Tell me more.",
            f"I can imagine how annoying that must be! {self.personality.random_emoji()} What happened next?",
            f"Ugh, that would drive me crazy too! {self.personality.random_emoji()} Continue!",
            f"*nodding along* {self.personality.random_emoji()} I'm tracking with you. Keep going!",
        ]

        await message.channel.send(random.choice(followup_responses))

    async def handle_rant_response(self, message):
        """Handle responses when someone is actively ranting"""
        # Validating responses for ongoing rants
        validations = [
            f"Uh-huh, I hear you! {self.personality.random_emoji()} That's totally valid.",
            f"Oh wow, yeah that's infuriating! {self.personality.random_emoji()} Keep going!",
            f"I can see why that would upset you! {self.personality.random_emoji()} What else?",
            f"Right?! That's so annoying! {self.personality.random_emoji()} Tell me more.",
            f"Absolutely! That would bother me too! {self.personality.random_emoji()} Continue!",
            f"I'm with you on this one! {self.personality.random_emoji()} That sounds terrible!",
            f"Valid feelings! {self.personality.random_emoji()} I'm still listening!",
            f"*nodding vigorously* {self.personality.random_emoji()} Yes! What happened then?",
            f"Oh no they didn't! {self.personality.random_emoji()} That's wild!",
            f"I'm getting secondhand frustration just hearing this! {self.personality.random_emoji()}",
        ]

        # Random chance to respond with validation (30% of the time)
        if random.random() < 0.3:
            await message.channel.send(random.choice(validations))

    async def end_rant_zone(self, message):
        """Wrap up the rant session"""
        closing_responses = [
            f"Thank you for trusting me with all that! {self.personality.random_emoji()} I heard every word. ♡",
            f"Wow, you got a lot out! {self.personality.random_emoji()} How are you feeling now? ♡", 
            f"I'm glad you could vent all that out! {self.personality.random_emoji()} You're heard and valid. ♡",
            f"That was a lot to carry around! {self.personality.random_emoji()} I hope getting it out helped. ♡",
            f"Sometimes we just need someone to listen. {self.personality.random_emoji()} I'm honored you chose me. ♡",
        ]

        await message.channel.send(random.choice(closing_responses))
        await asyncio.sleep(1)

        # Offer next steps
        next_steps = [
            f"Want to do something to decompress? Maybe a study session or some self-care? {self.personality.random_emoji()}",
            f"How about we shift gears? I could get you some news, or we could do a breathing exercise? {self.personality.random_emoji()}",
            f"Ready for something different? Maybe some weather or a productive distraction? {self.personality.random_emoji()}",
        ]

        await message.channel.send(random.choice(next_steps))

        # Reset rant mode
        self.rant_mode_active = False

    async def general_care(self, message):
        """General caring response"""
        caring_responses = [
            f"I'm here if you need anything, senpai. {self.personality.random_emoji()} You matter to me. ♡",
            f"Just wanted you to know - you're doing great! {self.personality.random_emoji()} I believe in you. ♡",
            f"Remember to be gentle with yourself today. {self.personality.random_emoji()} You deserve kindness. ♡",
            f"I care about you! {self.personality.random_emoji()} Don't forget to take care of yourself. ♡",
            f"You're stronger than you know, and softer than you think you should be. Both are perfect. {self.personality.random_emoji()} ♡",
        ]

        await message.channel.send(random.choice(caring_responses))
