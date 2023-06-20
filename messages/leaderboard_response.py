import discord

def leaderboard_embed(leaderboard):
    """Create an embed for the leaderboard.

    :param leaderboard: A list of the top players.
    :return: An Embed object.
    """
    embed = discord.Embed(title="Leaderboard", description="The highest rated players", color=0x00ff00)

    # Loop through the players in the leaderboard and add each one to the embed
    for i, player in enumerate(leaderboard, start=1):
        embed.add_field(name=f"{i}. {player['d_name']}", value=f"Rating: {player['rating']}", inline=False)

    return embed
