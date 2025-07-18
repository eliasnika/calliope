import asyncio
import re
import random
from datetime import datetime, timedelta

class PomodoroTimer:
    """Individual timer instance"""
    def __init__(self, user_id, duration_minutes, timer_type="study"):
        self.user_id = user_id
        self.duration_minutes = duration_minutes
        self.timer_type = timer_type
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=duration_minutes)
        self.is_active = True
        self.task = None

    def time_remaining(self):
        if not self.is_active:
            return 0
        remaining = self.end_time - datetime.now()
        return max(0, remaining.total_seconds() / 60)

    def stop(self):
        self.is_active = False
        if self.task:
            self.task.cancel()

class PomodoroFeature:
    """Handles pomodoro timers with natural language"""

    def __init__(self, personality):
        self.personality = personality
        self.active_timers = {}

        # All the natural language patterns
        self.timer_patterns = [
            # Study patterns
            r"let'?s study for (\d+) minutes?",
            r"study for (\d+) minutes?",
            r"study (\d+) minutes?",
            r"study (\d+) min",
            r"study (\d+)m",
            r"(\d+) min study",
            r"(\d+)m study",
            r"focus for (\d+) minutes?",
            r"focus (\d+) minutes?",
            r"work for (\d+) minutes?",
            r"pomo (\d+)",
            r"pomodoro (\d+)",
            r"timer for (\d+)",
            r"(\d+) minute timer",
            r"start timer for (\d+)",
            r"(\d+) minute study",
            r"grind for (\d+)",
            r"i want to study for (\d+)",
            r"gonna study for (\d+)",
            r"studying for (\d+)",
        ]

        self.break_patterns = [
            r"let'?s take a (\d+) minute break",
            r"break for (\d+) minutes?",
            r"(\d+) minute break",
            r"break (\d+) minutes?",
            r"break (\d+) min",
            r"break (\d+)m",
            r"(\d+) min break",
            r"(\d+)m break",
            r"chill for (\d+) minutes?",
            r"rest for (\d+) minutes?",
            r"relax for (\d+) minutes?",
            r"i need a (\d+) minute break",
            r"take a (\d+) minute break",
        ]

        self.status_patterns = [
            r"time left",
            r"time remaining",
            r"how much left",
            r"how long left",
            r"status",
            r"progress",
            r"timer status",
            r"check timer",
            r"how much time",
            r"how long until",
            r"when will i be done",
        ]

        self.stop_patterns = [
            r"stop",
            r"cancel",
            r"end",
            r"done",
            r"finished",
            r"quit",
            r"abort",
            r"halt",
            r"stop timer",
            r"cancel timer",
            r"i'm done",
            r"that's enough",
        ]

    async def can_handle(self, message):
        """Check if this feature can handle the message"""
        # Check for any pomodoro-related keywords
        keywords = [
            'study', 'focus', 'work', 'timer', 'pomodoro', 'pomo', 'break',
            'rest', 'chill', 'relax', 'status', 'progress', 'stop', 'done',
            'finished', 'cancel', 'time', 'minutes', 'min', 'grind'
        ]

        return any(keyword in message.lower() for keyword in keywords)

    async def handle(self, message):
        """Handle pomodoro-related messages"""
        content = message.content.lower().strip()

        # Check for timer start (study)
        for pattern in self.timer_patterns:
            match = re.search(pattern, content)
            if match:
                duration = int(match.group(1))
                await self.start_timer(message, duration, "study")
                return

        # Check for break timer
        for pattern in self.break_patterns:
            match = re.search(pattern, content)
            if match:
                duration = int(match.group(1))
                await self.start_timer(message, duration, "break")
                return

        # Check for status
        for pattern in self.status_patterns:
            if re.search(pattern, content):
                await self.check_status(message)
                return

        # Check for stop
        for pattern in self.stop_patterns:
            if re.search(pattern, content):
                await self.stop_timer(message)
                return

        # If no specific pattern matches, give a helpful response
        await message.channel.send(
            f"I think you want to do something with timers! {self.personality.random_emoji()}\n"
            f"Try saying: 'study for 25 minutes' or 'take a 5 minute break'!"
        )

    def get_help(self):
        """Return help text for this feature"""
        return """**🍅 Pomodoro Timer:**
• **Study:** "let's study for 25 minutes", "focus for 30 min", "pomo 25m"
• **Break:** "take a 5 minute break", "chill for 10 minutes", "break 15m"
• **Status:** "time left?", "progress check", "how much more?"
• **Stop:** "stop timer", "done", "cancel"
"""

    async def start_timer(self, message, duration, timer_type):
        """Start a new timer"""
        user_id = message.author.id

        # Check if user already has active timer
        if user_id in self.active_timers and self.active_timers[user_id].is_active:
            await message.channel.send(
                self.personality.error_response("already_active")
            )
            return

        # Validate duration
        if duration < 1 or duration > 240:
            await message.channel.send(
                self.personality.error_response("duration")
            )
            return

        # Create timer
        timer = PomodoroTimer(user_id, duration, timer_type)
        self.active_timers[user_id] = timer

        # Send confirmation
        response = self.personality.success_response(
            "timer_start", 
            duration=duration, 
            timer_type=timer_type
        )
        await message.channel.send(response)

        # Random encouragement (70% chance)
        if random.random() < 0.7:
            await asyncio.sleep(1)
            await message.channel.send(self.personality.encouragement())

        # Start countdown
        timer.task = asyncio.create_task(self.timer_countdown(message, timer))

    async def timer_countdown(self, message, timer):
        """Handle timer countdown"""
        try:
            # Wait for timer duration
            await asyncio.sleep(timer.duration_minutes * 60)

            if timer.is_active:
                # Timer completed
                response = self.personality.success_response(
                    "timer_complete",
                    duration=timer.duration_minutes,
                    timer_type=timer.timer_type
                )
                await message.channel.send(response)

                # Suggest next action
                await asyncio.sleep(1)
                if timer.timer_type == "study":
                    suggestion = self.personality.suggestion("break_after_study")
                else:
                    suggestion = self.personality.suggestion("study_after_break")
                await message.channel.send(suggestion)

                # Clean up
                timer.stop()
                if timer.user_id in self.active_timers:
                    del self.active_timers[timer.user_id]

        except asyncio.CancelledError:
            # Timer was cancelled - this is normal
            pass

    async def check_status(self, message):
        """Check timer status"""
        user_id = message.author.id

        if user_id not in self.active_timers or not self.active_timers[user_id].is_active:
            await message.channel.send(
                self.personality.success_response("no_timer")
            )
            return

        timer = self.active_timers[user_id]
        remaining = timer.time_remaining()

        if remaining <= 0:
            await message.channel.send(
                f"Perfect timing! {self.personality.random_emoji()} Your timer just finished!"
            )
            return

        # Format time remaining
        remaining_mins = int(remaining)
        remaining_secs = int((remaining - remaining_mins) * 60)

        if remaining_mins > 0:
            time_str = f"{remaining_mins} minute{'s' if remaining_mins != 1 else ''}"
            if remaining_secs > 0:
                time_str += f" and {remaining_secs} second{'s' if remaining_secs != 1 else ''}"
        else:
            time_str = f"{remaining_secs} second{'s' if remaining_secs != 1 else ''}"

        response = self.personality.success_response(
            "timer_status",
            time_str=time_str,
            timer_type=timer.timer_type
        )
        await message.channel.send(response)

    async def stop_timer(self, message):
        """Stop active timer"""
        user_id = message.author.id

        if user_id not in self.active_timers or not self.active_timers[user_id].is_active:
            await message.channel.send(
                self.personality.success_response("no_timer")
            )
            return

        timer = self.active_timers[user_id]
        timer.stop()
        del self.active_timers[user_id]

        response = self.personality.success_response(
            "timer_stopped",
            timer_type=timer.timer_type
        )
        await message.channel.send(response)
