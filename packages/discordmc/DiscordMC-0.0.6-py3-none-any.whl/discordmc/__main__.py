from .cli import *

server = Server('server.jar')
server.start()

bot = MCBot('m!')
parser = DiscordMCParser(bot, server)
threading.Thread(target=parser.watch_for_events).start()

threading.Thread(target=bot.add_cog, args=[MC(bot)]).start()
bot.server = server
bot.channel_id = 709367114598711348
bot.run('NTk3MTgxOTgxNzkyNDAzNDc3.XSEXDw.yLPcpmFgXKyiLJoeS3jh-0PDz_Y')
