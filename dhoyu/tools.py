
from .models import User, Card, Game

def get_card(user: User, game: Game) -> Card:
    '''
    returns a Card for this user and game
    creates a new one if one doesn't exist
    '''
    card = Card.query.filter_by(game=game).filter_by(user=user).one_or_none()
    if card is None:
        return Card(user, game)
    return card
