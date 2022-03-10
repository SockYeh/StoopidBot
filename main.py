import json, discord, requests, asyncio
from bs4 import BeautifulSoup
from discord.ext import commands
from discord_webhook import DiscordWebhook, DiscordEmbed

with open("config.json") as f:
    config = json.load(f)
TOKEN = config["token"]
WEBHOOK_URL = config["webhook_url"]
HATS = {
    "pirate legend": {"smallbox": "0.005", "biggift": "0.11", "area": "6"},
    "ice cream beanie": {"smallbox": "0.004", "biggift": "0.09", "area": "7"},
    "sparkle wings": {"smallbox": "0.006", "biggift": "0.13", "area": "8"},
    "monster dominus": {"smallbox": "0.002", "biggift": "0.06", "area": "9"},
    "egg patch": {"smallbox": "0.004", "biggift": "0.09", "area": "10"},
    "penguin": {"smallbox": "0.002", "biggift": "0.06", "area": "11"},
    "fire headdress": {"smallbox": "0.002", "biggift": "0.06", "area": "12"},
    "mr robot": {"smallbox": "0.003", "biggift": "0.07", "area": "13"},
    "matrix valkyrie": {"smallbox": "0.003", "biggift": "0.07", "area": "14"},
    "the sun king": {"smallbox": "0.003", "biggift": "0.07", "area": "15"},
    "rubber duckie": {"smallbox": "0.003", "biggift": "0.07", "area": "16"},
    "majestic leaf wings": {"smallbox": "0.003", "biggift": "0.07", "area": "17"},
    "traffic cone": {"smallbox": "0.003", "biggift": "0.07", "area": "18"},
    "ninja headband": {"smallbox": "0.003", "biggift": "0.07", "area": "19"},
    "ascii white": {"smallbox": "0.003", "biggift": "0.07", "area": "20"},
    "chicken master": {"smallbox": "0.003", "biggift": "0.07", "area": "21"},
    "dominus empyreus": {"smallbox": "0.003", "biggift": "0.07", "area": "22"},
    "golden top hat": {"smallbox": "0.003", "biggift": "0.07", "area": "23"},
    "illusion master": {"smallbox": "0.003", "biggift": "0.07", "area": "24"},
    "fairy king's wings": {"smallbox": "0.003", "biggift": "0.07", "area": "25"},
    "dragonfly wings": {"smallbox": "0.003", "biggift": "0.07", "area": "26"},
    "microwave": {"smallbox": "0.003", "biggift": "0.07", "area": "27"},
    "lol balloon": {"smallbox": "0.003", "biggift": "0.07", "area": "28"},
    "the kings adornments": {"smallbox": "0.003", "biggift": "0.07", "area": "29"},
    "alien commander": {"smallbox": "0.003", "biggift": "0.07", "area": "30"},
    "lightbulb": {"smallbox": "0.003", "biggift": "0.07", "area": "31"},
    "sinister pumpkin": {"smallbox": "0.003", "biggift": "0.07", "area": "32"},
    "pumpking": {"smallbox": "0.003", "biggift": "0.07", "area": "33"},
    "ghost wings": {"smallbox": "0.003", "biggift": "0.07", "area": "34"},
    "pixel king": {"smallbox": "0.003", "biggift": "0.07", "area": "35"},
    "phonograph": {"smallbox": "0.003", "biggift": "0.07", "area": "36"},
    "sea king's trident": {"smallbox": "0.003", "biggift": "0.07", "area": "37"},
    "morning coffee": {"smallbox": "0.003", "biggift": "0.07", "area": "38"},
    "voidwrath": {"smallbox": "0.003", "biggift": "0.07", "area": "39"},
    "santa's bag": {"smallbox": "0.003", "biggift": "0.07", "area": "40"},
    "fallen ice wings": {"smallbox": "0.003", "biggift": "0.07", "area": "41"},
    "polaris wings": {"smallbox": "0.003", "biggift": "0.07", "area": "42"},
    "snow king": {"smallbox": "0.003", "biggift": "0.07", "area": "43"},
    "empyrean reignment": {"smallbox": "0.003", "biggift": "0.07", "area": "44"},
    "demonic greatsword": {"smallbox": "0.003", "biggift": "0.07", "area": "45"},
    "perfect creation": {"smallbox": "0.003", "biggift": "0.07", "area": "46"},
    "horse head": {"smallbox": "0.003", "biggift": "0.07", "area": "47"},
    "book wings": {"smallbox": "0.003", "biggift": "0.07", "area": "48"},
    "honey crown": {"smallbox": "0.003", "biggift": "0.07", "area": "49"},
    "knowledge key": {"smallbox": "0.003", "biggift": "0.07", "area": "50"},
    "flying meteor": {"smallbox": "0.003", "biggift": "0.07", "area": "51"},
    "ba na na": {"smallbox": "0.003", "biggift": "0.07", "area": "52"},
    "do mi no": {"smallbox": "0.003", "biggift": "0.07", "area": "53"},
    "artificial heart": {"smallbox": "0.003", "biggift": "0.07", "area": "54"},
    "steampunk axe": {"smallbox": "0.003", "biggift": "0.07", "area": "55"},
    "roblox delicacy": {"smallbox": "0.003", "biggift": "0.07", "area": "56"},
    "dominus infernus": {"smallbox": "0.002", "biggift": "0.06", "area": "57"},
    "blazing aura": {"smallbox": "0.002", "biggift": "0.06", "area": "57"},
    "tonk": {"smallbox": "0.002", "biggift": "0.06", "area": "58"},
    "not a roller coaster": {"smallbox": "0.002", "biggift": "0.06", "area": "58"},
    "emotimask": {"smallbox": "0.002", "biggift": "0.06", "area": "59"},
    "full battery": {"smallbox": "0.002", "biggift": "0.06", "area": "59"},
    "cyber arms": {"smallbox": "0.0013", "biggift": "0.03", "area": "60"},
    "mythical angel": {"smallbox": "0.0013", "biggift": "0.03", "area": "60"},
    "supercharged aura": {"smallbox": "0.0013", "biggift": "0.03", "area": "60"},
}


bot = commands.Bot(
    command_prefix="-",
    intents=discord.Intents.all(),
    case_insensitive=False,
    help_command=None,
)


@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, asyncio.TimeoutError):
        await ctx.channel.send("Timed out. Please rerun the command!")


@bot.command()
async def start(ctx):
    e = discord.Embed(
        title="Unboxing Global Item Recreator",
        description="Do you want to recreate an egg hatch or a hat unbox? 1 for hatch and 2 for unbox. Defaults to hatch.",
        color=0xFFA500,
    )
    e.set_footer(
        text=f"Command invoked by {ctx.author} | Made by SockYeh#0001",
        icon_url=ctx.author.avatar_url,
    )
    await ctx.send(embed=e)
    msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author)
    match msg.content:
        case "2":
            hatch_or_unbox = "Unbox"
            avatarurl = "https://cdn.discordapp.com/avatars/890338927846772786/17fc650643084ae85ac64691a3d2149f.webp?size=80"
            webhook = DiscordWebhook(
                url=WEBHOOK_URL, username=hatch_or_unbox, avatar_url=avatarurl
            )
            wembed = DiscordEmbed()
            e = discord.Embed(
                title="Unboxing Global Item Recreator",
                description="Please provide your roblox account ID.",
                color=0xFFA500,
            )
            e.set_footer(
                text=f"Command invoked by {ctx.author} | Made by SockYeh#0001",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=e)
            usrid = await bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            try:
                usrid = int(usrid.content)
                r = requests.get(f"https://www.roblox.com/users/{usrid}/profile")
                soup = BeautifulSoup(r.text, "html.parser")
                dname = soup.find(
                    "h2", class_="profile-name text-overflow"
                ).text.strip()
                rname = soup.find(
                    "div",
                    class_="profile-display-name font-caption-body text text-overflow",
                ).text.strip()

                r = requests.post(
                    "https://thumbnails.roblox.com/v1/batch",
                    json=[
                        {
                            "requestId": f"{usrid}::AvatarHeadshot:150x150:png:regular",
                            "type": "AvatarHeadShot",
                            "targetId": int(usrid),
                            "token": "",
                            "format": "png",
                            "size": "150x150",
                        }
                    ],
                )
                imgurl = r.json()["data"][0]["imageUrl"]
                wembed.set_author(url=imgurl, name=f"{dname}({rname})", icon_url=imgurl)
            except Exception:
                await ctx.channel.send("Invalid user id!")
                return

            e = discord.Embed(
                title="Unboxing Global Item Recreator",
                description="Please provide the name of the hat you want to recreate the embed for.",
                color=0xFFA500,
            )

            e.set_footer(
                text=f"Command invoked by {ctx.author} | Made by SockYeh#0001",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=e)
            hpname = await bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            wembed.add_embed_field(name="Name", value=hpname.content, inline=True)

            e = discord.Embed(
                title="Unboxing Global Item Recreator",
                description="Please provide the box from which you want to unbox the hat from. 1 for small box and 2 for big gift. Defaults to small box.",
                color=0xFFA500,
            )

            e.set_footer(
                text=f"Command invoked by {ctx.author} | Made by SockYeh#0001",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=e)
            hpchance = await bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            match hpchance.content:
                case "2":

                    chance = str(
                        int(100 / float(HATS[hpname.content.lower()]["biggift"]))
                    )
                    chance = chance[0:-3]
                    wembed.add_embed_field(
                        name="Chance",
                        value=f'1 in {chance}k ({HATS[hpname.content.lower()]["biggift"]}%)',
                        inline=True,
                    )
                    match chance:
                        case "25" | "20":
                            wembed.set_color(0xFF6600)
                    wembed.add_embed_field(
                        name="Location",
                        value=f"Big Gift ({HATS[hpname.content.lower()]['area']})",
                        inline=True,
                    )

                case _:
                    chance = str(
                        int(100 / float(HATS[hpname.content.lower()]["smallbox"]))
                    )
                    chance = chance[0:-3]
                    wembed.add_embed_field(
                        name="Chance",
                        value=f'1 in {chance}k ({HATS[hpname.content.lower()]["smallbox"]}%)',
                        inline=True,
                    )
                    match chance:
                        case "33" | "50":
                            wembed.set_color(0xFF0000)
                        case "25":
                            wembed.set_color(0xFF6600)
                        case "76":
                            wembed.set_color(0xCC00FF)

                    wembed.add_embed_field(
                        name="Location",
                        value=f"Big Gift ({HATS[hpname.content.lower()]['area']})",
                        inline=True,
                    )
            webhook.add_embed(wembed)
            webhook.execute()
        case _:
            hatch_or_unbox = "Hatch"
            avatarurl = "https://cdn.discordapp.com/avatars/890338927846772786/3ace9899a88b35e4a66e16049114496f.webp?size=80"
            webhook = DiscordWebhook(
                url=WEBHOOK_URL, username=hatch_or_unbox, avatar_url=avatarurl
            )
            wembed = DiscordEmbed()
            e = discord.Embed(
                title="Unboxing Global Item Recreator",
                description="Please provide your roblox account ID.",
                color=0xFFA500,
            )
            e.set_footer(
                text=f"Command invoked by {ctx.author} | Made by SockYeh#0001",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=e)
            usrid = await bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            try:
                usrid = int(usrid.content)
                r = requests.get(f"https://www.roblox.com/users/{usrid}/profile")
                soup = BeautifulSoup(r.text, "html.parser")
                dname = soup.find(
                    "h2", class_="profile-name text-overflow"
                ).text.strip()
                rname = soup.find(
                    "div",
                    class_="profile-display-name font-caption-body text text-overflow",
                ).text.strip()

                r = requests.post(
                    "https://thumbnails.roblox.com/v1/batch",
                    json=[
                        {
                            "requestId": f"{usrid}::AvatarHeadshot:150x150:png:regular",
                            "type": "AvatarHeadShot",
                            "targetId": int(usrid),
                            "token": "",
                            "format": "png",
                            "size": "150x150",
                        }
                    ],
                )
                imgurl = r.json()["data"][0]["imageUrl"]
                wembed.set_author(url=imgurl, name=f"{dname}({rname})", icon_url=imgurl)
            except Exception:
                await ctx.channel.send("Invalid user id!")
                return

            e = discord.Embed(
                title="Unboxing Global Item Recreator",
                description="Please provide the name of the pet you want to recreate the embed for.",
                color=0xFFA500,
            )

            e.set_footer(
                text=f"Command invoked by {ctx.author} | Made by SockYeh#0001",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=e)
            hpname = await bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )
            wembed.add_embed_field(name="Name", value=hpname.content, inline=True)

            e = discord.Embed(
                title="Unboxing Global Item Recreator",
                description="Please provide the chances (in %) of the pet you want to recreate the embed for.",
                color=0xFFA500,
            )
            e.set_footer(
                text=f"Command invoked by {ctx.author} | Made by SockYeh#0001",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.send(embed=e)
            hpchance = await bot.wait_for(
                "message", check=lambda m: m.author == ctx.author
            )

            match hpchance.content.replace("%", ""):
                case "0.0001":
                    wembed.set_color(0x00FF00)
                    wembed.add_embed_field(
                        name="Chance",
                        value=f"1 in 1M ({hpchance.content}%)",
                        inline=True,
                    )
                case "0.0004":
                    wembed.set_color(0x00FF00)
                    wembed.add_embed_field(
                        name="Chance",
                        value=f"1 in 250k ({hpchance.content}%)",
                        inline=True,
                    )
                case "0.002":
                    wembed.set_color(0xCC00FF)
                    wembed.add_embed_field(
                        name="Chance",
                        value=f"1 in 50k ({hpchance.content}%)",
                        inline=True,
                    )
                case "0.0017":
                    wembed.set_color(0xCC00FF)
                    wembed.add_embed_field(
                        name="Chance",
                        value=f"1 in 57k ({hpchance.content}%)",
                        inline=True,
                    )
                case _:
                    await ctx.channel.send("Invalid chance!")
                    return
            webhook.add_embed(wembed)
            webhook.execute()


bot.run(TOKEN)
