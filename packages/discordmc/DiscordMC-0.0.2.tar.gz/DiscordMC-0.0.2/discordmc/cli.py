import click
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



@click.command(name='mcs', help='Runs the server')
@click.argument('jar_path')
@click.argument('token')
@click.argument('channel_id')
def cli(jar_path, token, channel_id):
    server = Server(jar_path)
    server.start()

    bot = MCBot('m!')
    parser = DiscordMCParser(bot, server)
    threading.Thread(target=parser.wait_for_events).start()

    bot.add_cog(MC)
    bot.server = server
    bot.channel_id = channel_id
    bot.run(token)



