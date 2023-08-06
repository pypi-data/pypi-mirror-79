from mcserverapi import Server, Parser
from .bot import MC, MCBot
import threading


class DiscordMCParser(Parser):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    def on_ready(self, ctx):
        self.bot.announce('Server started in {}'.format(ctx[0]))

    def on_player_message(self, ctx):
        player, message = ctx
        self.bot.message_queue[message] = {
            'sent': False,
            'player': player
        }




