import discord


def calculate_expected_elo(p1_rating: int, p2_rating: int):
    """
    :param p1_rating: Player 1 Rating
    :param p2_rating: Player 2 Rating
    :return:
    expected, expected
    """
    q1 = 10**(p1_rating/400)
    q2 = 10**(p2_rating/400)

    e1 = q1/(q1+q2)
    e2 = 1 - e1
    return e1, e2


def calculate_rating_change(rating: int, expected: float, wins: int, total_games: int):
    k = 32
    difference = round(k * total_games * ((wins/total_games) - expected))
    return rating, difference


def calculate_match(p1: (int, int), p2: (int, int)):
    """
    :param p1:
    (rating, wins)
    :param p2:
    (rating, wins)
    :return:
    """
    expectations = calculate_expected_elo(p1[0], p2[0])

    total_games = p1[1] + p2[1]
    p1_change = calculate_rating_change(p1[0], expectations[0], p1[1], total_games)
    p2_change = calculate_rating_change(p2[0], expectations[1], p2[1], total_games)

    return p1_change, p2_change

