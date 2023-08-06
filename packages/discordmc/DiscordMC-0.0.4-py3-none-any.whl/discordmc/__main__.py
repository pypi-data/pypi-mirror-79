from .cli import *


server = Server('server.jar')
server.start()

bot = MCBot('m!')
parser = DiscordMCParser(bot, server)
threading.Thread(target=parser.wait_for_events).start()

bot.add_cog(MC)
bot.server = server
bot.channel_id = 709367114598711348
bot.run('NTk3MTgxOTgxNzkyNDAzNDc3.XSEXDw.yLPcpmFgXKyiLJoeS3jh-0PDz_Y')