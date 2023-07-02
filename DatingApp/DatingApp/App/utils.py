from .models import Sympathy


def check_sympathy(from_user, to_user):
    try:
        Sympathy.objects.get(from_user=from_user, to_user=to_user)
        Sympathy.objects.get(from_user=to_user, to_user=from_user)
        return True  # Симпатия найдена
    except Sympathy.DoesNotExist:
        return False  # Симпатия не найдена