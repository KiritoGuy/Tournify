import asyncio
from discord import Embed
from config import MAIN_COLOR, RED_COLOR, HEADER



def success_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=MAIN_COLOR
    )


def invisible_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=0x2f3136
    )


def error_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=RED_COLOR
    )

async def create_channel(self, c_name, *, guild, overwrites, category):
    channel = await guild.create_text_channel(name=c_name, overwrites=overwrites, category=category)
    return await channel.send(embed=success_embed(HEADER, f"CHANNEL CREATED: {c_name}")

async def create_role_func(self, guild, *, r_name):
    role = await guild.create_role(name=f"{r_name}")
    if role:
        print("ROLE CREATED: {r_name}")
        return role

async def give_role(self, member: discord.Member, role):
    await member.add_roles(role)
    print(f"Role assigned to: {member.display_name}")

async def assign_role(self, role, df, name, ctx):
    e = discord.Embed()
    result_id = []
    unreachable_users = []
    # gets index of row
    index, = df.index[df["channel_name"] == name]
    # if multiple member ids are given
    if len(df.index) > 0:
        try:
            result_id = df.loc[index, 'member_ids'].split(", ")
            for i in range(0, len(result_id)):
                result_id[i] = int(result_id[i])
        except:
            pass
    # if only single member id is provided
    else:
        result_id = int(df.loc[index, 'member_ids'])

    for result in result_id:
        try:
            member = ctx.guild.get_member(result)
            if get(member.roles, id=role.id):
                continue
            await self.give_role(member=member, role=role)
            e = Embed(description="You have been assigned **{role}**!\nCheck **{name}** channel under the ***TOURNAMENT*** category for updates on the tourney.", color=MAIN_COLOR)
            await member.send(embed=e)
        # if member has dm off or if they are not in the server
        except:
            unreachable_users.append(result)
        result_id.clear()

    if unreachable_users:
        while "" in unreachable_users:
            unreachable_users.remove("")
        users_string = ' '.join(str(x) for x in unreachable_users).split(" ")
        e = Embed(description="Member(s) with this id: **{', '.join(x for x in users_string)}** are not reachable."
        await ctx.send(embed=e)

    async def get_data_from_db(self):
        names = []
        # keep_default_na = False, to reject nan values
        df = pd.read_csv(self.URL, keep_default_na=False)

        for number in range(len(df.index)):
            # gets channel names from the column channel_name in the db
            channel_name = df.loc[number, 'channel_name']
            if "" == channel_name:
                continue
            names.append(channel_name)

        return names, df
