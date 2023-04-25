import discord


def rating_embed(user: discord.Member, rating) -> discord.Embed:
    embed = discord.Embed(
        title=f"{user.display_name}'s rating",
        description=f'{rating}',
        colour=0x00ff95
    ).add_field(
        name='WINS',
        value='0',
        inline=True
    ).add_field(
        name='LOSSES',
        value='0',
        inline=True
    ).set_thumbnail(
        url=user.avatar.url if user.avatar else 'https://cdn.discordapp.com/embed/avatars/0.png'
    )

    return embed
