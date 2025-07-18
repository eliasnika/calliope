import random

class VTuberPersonality:
    """All the kawaii expressions and consistent responses"""

    def __init__(self):
        # Core expressions
        self.mood_emojis = [
            "(´｡• ᵕ •｡`)", "(◕‿◕)", "( ´ ω ` )", "ヽ(°〇°)ﾉ", 
            "(◡ ‿ ◡)", "(*´꒳`*)", "( ◞･̀∩･́)◞", "♡(˃͈ દ ˂͈ ༶ )"
        ]

        self.excitement_emojis = [
            "✧(◕‿-)✧", "٩(◕‿◕)۶", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", 
            "ヽ(♡‿♡)ノ", "┌(★ｏ☆)┘", "＼(^o^)／"
        ]

        self.supportive_emojis = [
            "(つ✧ω✧)つ", "(づ｡◕‿‿◕｡)づ", "＼(^▽^)／", 
            "ヾ(＾-＾)ノ", "(｡•̀ᴗ-)✧"
        ]

        # NEW: Error and weather-specific expressions!
        self.error_emojis = [
            "(◞‸◟)", "(｡•́︿•̀｡)", "(´-ω-`)", "( ˘︹˘ )", 
            "(｡╯︵╰｡)", "(´∩｡• ᵕ •｡∩`)", "(◞ ‸ ◟ )", "( ◡̦ ‿ ◡̦ )"
        ]

        self.cold_weather_emojis = [
            "(｡>﹏<｡)", "(◞ ‸ ◟ )", "( ˘︹˘ )", "(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥｀)", 
            "ヽ(°〇°)ﾉ", "(⌒_⌒;)"
        ]

        self.warm_weather_emojis = [
            "(◕‿◕)♡", "ヽ(°〇°)ﾉ", "＼(^▽^)／", "(｡◕‿◕｡)", 
            "ヾ(＾∇＾)", "( ◡ ‿ ◡ )", "(◔‿◔)", "✧(◕‿-)✧"
        ]

        # Response collections
        self.greetings = [
            "Hiya senpai! {} Ready to be productive together?",
            "Ohayo! {} What are we working on today?",
            "Senpai! {} I've been waiting for you!",
            "Konnichiwa! {} Let's make today amazing!",
            "Heya! {} Ready to tackle some work together?",
            "Yay! {} My favorite study buddy is back!",
        ]

        self.casual_responses = [
            "Mhm mhm! {} I'm listening~",
            "Oh really? {} Tell me more!",
            "Senpai~ {} You're so interesting!",
            "Aww! {} That's nice!",
            "I see, I see! {} Anything else on your mind?",
            "Hai hai! {} I'm here if you need anything!",
            "Hmm~ {} What should we do next?",
        ]

        self.encouragements = [
            "You've got this! {}",
            "I believe in you! {}",
            "Ganbatte senpai! {}",
            "Focus mode activated! {}",
            "Let's do this together! {}",
            "You're amazing! {}",
        ]

    def random_emoji(self):
        """Get a random cute emoji"""
        all_emojis = self.mood_emojis + self.excitement_emojis + self.supportive_emojis
        return random.choice(all_emojis)

    def get_error_emoji(self):
        """Get a sad emoji for errors"""
        return random.choice(self.error_emojis)

    def get_weather_emoji(self, temp):
        """Get appropriate emoji based on temperature"""
        if temp < 50:
            return random.choice(self.cold_weather_emojis)
        elif temp > 75:
            return random.choice(self.warm_weather_emojis)
        else:
            return random.choice(self.mood_emojis)

    def greeting(self):
        """Random greeting response"""
        template = random.choice(self.greetings)
        return template.format(random.choice(self.mood_emojis))

    def casual_response(self):
        """Random casual response"""
        template = random.choice(self.casual_responses)
        return template.format(random.choice(self.mood_emojis))

    def encouragement(self):
        """Random encouragement"""
        template = random.choice(self.encouragements)
        return template.format(random.choice(self.supportive_emojis))

    def unauthorized(self):
        """Response for unauthorized users"""
        return f"Eh? {random.choice(self.mood_emojis)} Sorry, but I only talk to my senpai! You're not them, are you? (◞‸◟)"

    def error_response(self, error_type="general"):
        """Error responses with personality"""
        if error_type == "duration":
            responses = [
                "Eh? {} That's a bit much! Try 1-240 minutes please~",
                "Ano... {} Let's keep it between 1-240 minutes, ok?",
                "Senpai~ {} That's too long! Pick something between 1-240 minutes!",
            ]
        elif error_type == "already_active":
            responses = [
                "Eh? {} You already have a timer running! Say 'stop' to cancel it first~",
                "Matte! {} There's already a timer going! Want to stop it first?",
                "Senpai~ {} You've got a timer active! Try 'done' to finish it!",
            ]
        else:
            responses = [
                "Eh? {} Something went wrong! Try again?",
                "Ano... {} I didn't understand that! Can you try differently?",
                "Gomen! {} I'm confused! What did you want to do?",
            ]

        template = random.choice(responses)
        return template.format(random.choice(self.mood_emojis))

    def success_response(self, action_type, **kwargs):
        """Success responses for different actions"""
        if action_type == "timer_start":
            duration = kwargs.get('duration', 0)
            timer_type = kwargs.get('timer_type', 'study')

            if timer_type == "study":
                responses = [
                    "Yay! {} {} minutes of study time! Let's goooo!",
                    "Okie dokie! {} {} minutes of focus time starting now!",
                    "Alright senpai! {} {} minutes of productive time!",
                    "Yosh! {} {} minutes of learning time! You got this!",
                ]
            else:  # break
                responses = [
                    "Break time! {} {} minutes to recharge~",
                    "Ooh rest time! {} {} minutes of chill vibes!",
                    "You deserve this! {} {} minutes of relaxation!",
                    "Time to chill! {} {} minutes of comfy time~",
                ]

            template = random.choice(responses)
            return template.format(random.choice(self.excitement_emojis), duration)

        elif action_type == "timer_complete":
            duration = kwargs.get('duration', 0)
            timer_type = kwargs.get('timer_type', 'study')

            if timer_type == "study":
                responses = [
                    "Yay! {} {} minutes of study complete! Senpai is amazing!",
                    "Woohoo! {} {} minutes of focus done! You're incredible!",
                    "Sugoi! {} {} minutes of study power! You did so well!",
                    "Yatta! {} {} minutes of focus time finished!",
                ]
            else:  # break
                responses = [
                    "Break time over! {} {} minutes of rest complete!",
                    "Refreshed? {} {} minutes of chill time done!",
                    "Ready to go? {} {} minutes of rest finished!",
                ]

            template = random.choice(responses)
            return template.format(random.choice(self.excitement_emojis), duration)

        elif action_type == "timer_status":
            time_str = kwargs.get('time_str', 'some time')
            timer_type = kwargs.get('timer_type', 'study')

            responses = [
                "You've got {} left! {} Keep going senpai!",
                "{} remaining! {} You're doing great!",
                "Just {} more! {} You're crushing it!",
                "{} left on your {} session! {} Ganbatte!",
            ]

            template = random.choice(responses[:3])  # First 3 don't need timer_type
            return template.format(time_str, random.choice(self.supportive_emojis))

        elif action_type == "timer_stopped":
            timer_type = kwargs.get('timer_type', 'study')

            responses = [
                "Stopped! {} Good work on that {} session!",
                "All done! {} Every bit of effort counts!",
                "No worries! {} You showed up and that's what matters!",
                "Session ended! {} You did great while it lasted!",
            ]

            template = random.choice(responses)
            return template.format(random.choice(self.mood_emojis), timer_type)

        elif action_type == "no_timer":
            responses = [
                "No timers running! {} Want to start one?",
                "All clear! {} Ready to begin a study session?",
                "Nothing active right now! {} Let's get productive!",
            ]

            template = random.choice(responses)
            return template.format(random.choice(self.mood_emojis))

        else:
            return f"Done! {random.choice(self.supportive_emojis)}"

    def suggestion(self, suggestion_type):
        """Suggestions for next actions"""
        if suggestion_type == "break_after_study":
            responses = [
                "Time for a break? {} Maybe 'let's take a 5 minute break'?",
                "How about some rest? {} Try 'break for 10 minutes'~",
                "Break time maybe? {} You deserve it!",
            ]
        elif suggestion_type == "study_after_break":
            responses = [
                "Feeling refreshed? {} Ready for another study session?",
                "Break's over! {} Time to dive back in!",
                "Ready to focus again? {} Let's gooo!",
            ]
        else:
            responses = [
                "What's next? {} I'm here to help!",
                "Ready for more? {} Let's keep going!",
            ]

        template = random.choice(responses)
        return template.format(random.choice(self.mood_emojis))
