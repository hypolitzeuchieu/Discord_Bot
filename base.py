
from discord import Intents
from discord.ext import commands

intents = Intents.all()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", description="try discord Bot", intents=intents)


@bot.event
async def on_ready():
    print(f"ready for {bot.user.name}...")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    salutation_name = ['hey', 'hi', 'hello']
    if message.content.lower() in salutation_name:
        await message.channel.send(f"hello **{message.author.display_name}** hope *you are fine*!")


@bot.event
async def on_member_join(member):
    try:
        general_channel = bot.get_channel(1214528710414307340)
        if general_channel:
            await general_channel.send(content=f"welcome **{member.display_name}** to this server **{member.guild.name}** this is a message of **{bot.user.name}**")
    except Exception as e:
        print(f"something went wrong : {e}")


bot.run("MTIxNDUyNjkyNjg2NjA5NjEzOA.GNq40n.Mq_fjoAOw8_sJ_pIkeRESb10ptmhyQ2vViq7bk")
