import discord


def match_result_embed(placement, ratings, match_id: str) -> discord.Embed:
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
        value=f'{ratings[0][0] + ratings[0][1]} ({ratings[0][1]}) / {ratings[1][0] + ratings[1][1]} ({ratings[1][1]})',
        inline=False
    ).set_footer(
        text=match_id
    )
    if not placement[2]:
        embed.set_thumbnail(
            url=placement[0][0].avatar.url if placement[0][0].avatar else 'https://cdn.discordapp.com/embed/avatars/0.png'
        )
    return embed
