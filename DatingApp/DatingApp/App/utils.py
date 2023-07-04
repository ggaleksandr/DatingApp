from geopy import distance

from .models import AppUser
from .models import Sympathy


def check_sympathy(from_user, to_user):
    try:
        Sympathy.objects.get(from_user=from_user, to_user=to_user)
        Sympathy.objects.get(from_user=to_user, to_user=from_user)
        return True  # Симпатия найдена
    except Sympathy.DoesNotExist:
        return False  # Симпатия не найдена


def calc_distance(from_user_id, to_user_id):
    from_user = AppUser.objects.get(id=from_user_id)
    to_user = AppUser.objects.get(id=to_user_id)

    coords_self = (from_user.lat, from_user.lng)
    coords_other = (to_user.lat, to_user.lng)

    dist = distance.distance(coords_self, coords_other).km

    return dist
