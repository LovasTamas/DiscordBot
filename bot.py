import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from myScheduler import myScheduler
from ScheduleItem import ScheduleItem
import datetime
import asyncio

myScheduler = myScheduler("Saves")
myScheduler.loadSchedule()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def info(ctx):
    await ctx.send("The following commands are available:\n\
                - !info : Gives addational information about commands usage.\n\n\
                - !addNewSchedule : Add a new item to the schedule table with the everyone tag. Usage: [!addNewSchedule hh:mm:ss h Message] Example: [!addNewSchedule 12:00:00 24 Hello my lovely cp!] would result in a repeating message of '@ everyone Hello my lovely cp!' every 24 hour. !!!Please note that only integers are accaptable as numbers, so no 3.5 and other tricky solutions!!!'\n\n\
                - !listSchedules : Gives a list about the scheduled items.\n\n\
                - !deleteSchedule : Remove a scheduled item. Usage: [!deleteSchedule ID] Example: [!deleteSchedule 5] would delete the ScheduleItem with ID 5. To get the responding ids use !listSchedules. !!!Please note that after deleting one item the IDs WILL probably change!!!")

@bot.command()
async def addNewSchedule(ctx, date, delay, *args):
    chnl = ctx.message.channel.id
    msg = " ".join(args)
    now = datetime.datetime.now()
    h, m, s = str(date).split(":")
    now = now.replace(hour=int(h), minute=int(m), second=int(s), microsecond=0)
    item = ScheduleItem(chnl, msg, now, delay)
    await ctx.send(f"Date was set to: {now}, the delay was set to: {delay}h, with the message of: {msg}")
    myScheduler.addScheduleItem(item)

@bot.command()
async def listSchedules(ctx):
    await ctx.send("The following items are scheduled:")
    if len(myScheduler.items) > 0:
        for item in myScheduler.items:
            await ctx.send(f"ID: {item.id}, message: {item.message}, delay: {item.delay}, the time of appearance: {item.time}")
    else:
        await ctx.send(f"There are no scheduled items!")

@bot.command()
async def deleteSchedule(ctx, id):
    result = myScheduler.removeItem(id)
    if result == True:
        await ctx.send(f"The item with the id of {id} has been permanently removed!")
    else:
        await ctx.send(f"Either there is no item with this id or there is an internal error, so the item wasn't deleted!")        

async def sendScheduledMessage():
    while True:
        for item in myScheduler.items:
            now = datetime.datetime.now()
            then = item.time + datetime.timedelta(hours=int(item.delay))
            wait_time = (then-now).total_seconds()
            print(wait_time)
            if wait_time <= 0:
                channel = bot.get_channel(item.channel)
                await channel.send("@everyone\n" + item.message)
                item.time = then
                myScheduler.updateIds()
            else:
                await asyncio.sleep(1)
        await asyncio.sleep(1)
    
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    await sendScheduledMessage()

def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    bot.run(TOKEN)