import discord
from discord.ext import commands
import datetime

bot_token = 'your_bot_token'

rosterCap = 24
coachRoles = commands.has_any_role('Franchise Owner', 'Head Coach', 'General Manager')
teams = ["Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills", "Carolina Panthers",
             "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns", "Dallas Cowboys", "Denver Broncos",
             "Detroit Lions", "Green Bay Packers", "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars",
             "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
             "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants", "New York Jets",
             "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers", "Seattle Seahawks",
             "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders", "Auburn Tigers", "Michigan Wolverines", "Alabama Crimson Tide", "North Carolina Tar Heels", "LSU Tigers"
             ,"Norte Dame Fighting Irish", "Florida Gators", "Baylor Bears", "Ohio State Buckeyes", "Oregon Ducks", "Oklahoma Sooners", "Penn State Nittany Lions"]


bot = commands.Bot(command_prefix=',', debug_guilds=[guild_id], intents=discord.Intents.all())

#note for guild_id if you want it to work in every server remove debug_guilds and the comma and wait about an hour


tranchanne = bot.get_channel(channel_id)


@bot.event
async def on_ready():
    print('online \n ---------------')
    
@bot.slash_command(description='force signs a member')
@coachRoles
async def sign(ctx, member: discord.Member):

    au = [role for role in ctx.author.roles]
    mem = [role for role in member.roles]

    for roles in mem:
        if roles.name in teams:
            await ctx.respond(f"that player is already in a team! \n > Team : `{roles.name}`", ephemeral=True)
            return

    for roles in au:
        if roles.name in teams:
            team = discord.utils.get(ctx.guild.roles, name=roles.name)

            if len(team.members) > rosterCap:
                await ctx.respond("max members in team", ephemeral=True)
                return

            try:
                await member.add_roles(team)
                free = discord.utils.get(ctx.guild.roles, name="Free Agent")
                await member.remove_roles(free)
            except:
                print("error with signing")
                break
            finally:
                da = team.name.replace(" ", "_")
                emoj = discord.utils.get(ctx.guild.emojis, name=f"{da}")
                e = discord.Embed(
                    title="New signing!",
                    description=f" > **A Team has signed a member.** \n > **Team** : {team.mention} \n > **Coach** : {ctx.author.mention} \n > **Roster limit** : `{len(team.members)}/{rosterCap}`",
                    color=team.color
                    )
                e.add_field(name="Player", value=f"{member.mention} `{member}`")
                e.set_thumbnail(url=emoj.url)
                await ctx.respond("signed member", ephemeral=True)
                await tranchanne.send(embed=e)
                return

@bot.slash_command(description='releases a member')
@coachRoles
async def release(ctx, member: discord.Member):
        auth = [role for role in ctx.author.roles]
        mem = [role for role in member.roles]

        for roles in mem:
            if roles.name in teams:
                team = discord.utils.get(ctx.guild.roles, name=roles.name)
                if team not in auth:
                    n = discord.Embed(
                        title="Unsuccessful!",
                        description=f"> **Author** {ctx.author.mention}"
                    )
                    n.add_field(name="Error Info",
                                value=f" > {member.mention} is in another team! \n > **Team** {team.mention}")

                    await ctx.respond(embed=n, ephemeral=True)
                    return


        for roles in mem:
            if roles.name in teams:
                team1 = discord.utils.get(ctx.guild.roles, name=roles.name)
                free = discord.utils.get(ctx.guild.roles, name='Free Agent')
                da = team1.name.replace(" ", "_")
                emoj = discord.utils.get(ctx.guild.emojis, name=f"{da}")
                await member.remove_roles(team1)
                try:
                    await ctx.message.delete()

                    await member.add_roles(free)

                except:
                    print(f"error at {datetime.datetime.utcnow()}")
                    return
                finally:
                    n = discord.Embed(title="Transaction Complete", description=f"> A team has released a player! \n > **Coach** {ctx.author.mention} `{ctx.author}`", color=team.color)
                    n.add_field(name="Team", value=f"> {team.mention}", inline=False)
                    n.add_field(name="Player", value=f"> {member.mention} `{member}`", inline=False)
                    n.set_thumbnail(url=emoj.url)
                    await tranchanne.send(embed=n)
                    await ctx.respond("released", ephemeral=True)
                    return
                

bot.run('bot_token')
