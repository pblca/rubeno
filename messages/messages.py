import discord


def match_result_embed(placement) -> discord.Embed:
    embed = discord.Embed(
        title='Match Results',
        description=f'{placement[0][1]} - {placement[1][1]}',
        colour=0x00ff95
    ).add_field(
        name='DRAW' if placement[2] else 'WIN',
        value=placement[0][0].mention,
        inline=True
    ).add_field(
        name='DRAW' if placement[2] else 'LOSS',
        value=placement[1][0].mention,
        inline=True
    ).add_field(
        name='Rating Update',
        value='1500 (+27) / 1250 (-12)',
        inline=False
    ).set_thumbnail(
        url=placement[0][0].avatar.url
    )
    return embed
