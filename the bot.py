import random
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="%", intents=intents)

@client.event
async def on_ready():  #פועלת כשהבוט מתחיל לרוץ, כשהוא הופך להיות אונליין
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("OverWatch 2"))
    print("I'm ready!")

@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user:
        return None
    await say(msg)
    await ani(msg)
    await mazalTov(msg)
    await botEmbed(msg)

@client.event
async def on_reaction_add(rea, user):
    msg = rea.message
    conMsg = msg.content.lower()
    emoji = str(rea)
    if(conMsg.startswith("hillel") and emoji == "👑"):
        await msg.channel.send(f"{user} - thanks!")

    if(emoji == "😇"):
        newConMsg = conMsg.replace("לא", "כן")
        await msg.edit(content=newConMsg)

@client.command()
async def embed(ctx):
    em = discord.Embed(title="אהלן אני מסי",
                       description="אני ניצחתי את המונדיאל",
                       color=678123)

    em.set_author(name="מסי",
                  icon_url="https://img.haarets.co.il/bs/0000017f-e550-dc7e-adff-f5fdc4af0000/3c/5c/09c6d6c686bccf9dd657b430ee53/366169293.jpg?precrop=1521,1520,x4,y21&height=700&width=700")
    em.set_image(
        url="https://media2.giphy.com/media/l3vR4Ell5crP9nYR2/giphy.gif?cid=ecf05e47b790e44817251a012dfe6317eedb86610e18ef6f&ep=v1_gifs_gifId&rid=giphy.gif&ct=g")
    await ctx.send(embed=em)

@client.command()
async def rand(ctx, num1=1, num2=10):
    num1 = int(num1)
    num2 = int(num2)
    str1 = str(random.randint(num1, num2))
    await ctx.send(str1)

@client.command()
async def bull(ctx):
    """
     משחקת איתך משחק של בול פגיעה
    בכל פעם תוכלו לנחש אחד מהצבעים הבאים
    ["🔴", "🔵", "🟣", "🟢", "🟡", "🟠"]
    כל פעם יישלחו האימוג'י 🎯 בשביל בול ו-💢 בשביל פגיעה
    """
    MAX_TRIES = 8 #כמה ניסיונות אפשר לפני שמפסידים
    colors = ["🔴", "🔵", "🟣", "🟢", "🟡", "🟠"]
    def checkMsg(msg):
        if (ctx.author == msg.author):  #ה-ctx.author הוא מי ששלח את הפקודה עצמה
            conMsg = msg.content
            conMsg = conMsg.replace(" ", "")
            for i in conMsg:
                if(not i in colors):
                    return False
        return True

    cho = random.sample(colors, k=4)
    tries = 0
    opEm = discord.Embed(title="ברוכים הבאים למשחק בול פגיעה!", #קיצור של opening embed - האמבד שנשלח בתחילת המשחק
                         description="במשחק הזה אתם תצטרכו למצוא את ארבעת הצבעים שבחרתי. מוזמנים לנחש את הניחוש הראשון שלכם!",
                         color=discord.Color.blue())
    opEm.set_image(url="https://d15djgxczo4v72.cloudfront.net/s3fs-public/styles/inner_page_header/public/legacy_files/565px-Mastermind.jpg?itok=pj8howAu")
    await ctx.send(embed=opEm)
    conMsg = ""
    choStr = "".join(cho)
    while(conMsg != choStr and tries <= MAX_TRIES):
        pgias = 0
        bulls = 0
        tries += 1
        msg = await client.wait_for("message", check=checkMsg)
        conMsg = msg.content
        conMsg = conMsg.replace(" ", "")
        for i in conMsg: #עובר על הצבעים בהודעה ששלחו לנו
            if (i in choStr): # בודק אם הצבע שניחשו בהודעה הוא אחד מהצבעים שהבוט בחר, כלומר פגיעה (יכול להיות פגיעה או בול)
                if(conMsg.find(i) == choStr.find(i)): #בודק אם הם באותו מיקום, כלומר בודק אם זה בול
                    bulls += 1 # אם כן, אז מוסיפים לכמות הבולים אחד
                else:
                    pgias += 1 # אם לא, אז זו פגיעה (כי ב-if הראשון כבר מצאנו שהצבע שניחשו הוא אחד מהצבעים שהבוט בחר, אז זה לפחות פגיעה)
        returnStr = "🎯" * bulls + "💢" * pgias # שם אימוג'ים לפי כמות הבולים והפגיעות
        await ctx.send(" " + returnStr)
    if(tries <= MAX_TRIES):
        winEm = discord.Embed(title="כל הכבוד! ניצחת!",
                              description=f"The sequence was {choStr}! It took you {tries} tries to guess it",
                              color=discord.Color.green())
        winEm.set_image(url="https://media4.giphy.com/media/lnlAifQdenMxW/giphy.gif?cid=ecf05e47w3qaugghkagdxyqbrlg2crypf1pd5vmyaxrsu2ab&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        await ctx.send(embed=winEm)
    else:
        losEm = discord.Embed(title="הפסדת...",
                              description=f"Don't worry, you can try again. The sequence was {choStr}.",
                              color=discord.Color.red())
        losEm.set_image(url="https://media4.giphy.com/media/dkuZHIQsslFfy/giphy.gif?cid=ecf05e47bkow9u5u32fuusfpfedq8gek60di64aydify4s29&ep=v1_gifs_search&rid=giphy.gif&ct=g")
        await ctx.send(embed=losEm)



async def mazalTov(msg):
    if "מזל טוב" in msg.content:
        await msg.add_reaction("🤠")
async def say(msg):
    conMsg = msg.content.lower()
    sayStr = "say "
    if(conMsg.startswith(sayStr)):
        await msg.channel.send(conMsg[len(sayStr):])
async def ani(msg):
    conMsg = msg.content.lower()
    aniStr = "אני "
    if(conMsg.find(aniStr) >= 0):
        await msg.channel.send(f"Hi {msg.author}, I'm the best bot ever")
async def botEmbed(msg):
    conMsg = msg.content.lower()
    em = discord.Embed(title="Hello, Hillel is here",
                       color=0xc8a0eb,
                       description="אהלן, נעים להכיר כאן הלל ואני הבוט שלכם להיום מה נשמע?")
    if (conMsg.startswith("em")):
        await msg.channel.send(embed=em)



client.run("MTA3MDM5Nzg1NzQ2ODc4ODc3Ng.GbZOP7.KUyG4vAoT5iKOV1tQy1_1Q_LWYuKcgpCyiGKvU")
