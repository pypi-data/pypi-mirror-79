from discord.ext.commands import command, Cog, Bot
import threading


class MCBot(Bot):
    async def on_message(self, message):
        if message.author != self.user:
            if not message.content.startswith(self.command_prefix):
                self.server.run_cmd('execute', 'as', message.author.nick, 'run', 'say', message.content)
            else:
                await self.process_commands(message)


class MC(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.message_queue = {}
        threading.Thread(target=self.bot.loop.call_soon_threadsafe, args=[self.bot.message_queue]).start()

    @command(name='mc')
    def mc(self, ctx, cmd, *params):
        self.bot.server.run_cmd('execute', 'as', ctx.author.nick, 'run', cmd, *params)

    async def message_worker(self):
        while self.bot.server.online:
            for message in self.bot.message_queue:
                if not self.bot.message_queue[message]['sent']:
                    await self.bot.get_channel(self.bot.channel_id).send(
                        '``' + self.bot.message_queue[message]['player'] + ' > ' + message + '``'
                    )
                    self.bot.message_queue[message]['sent'] = True
