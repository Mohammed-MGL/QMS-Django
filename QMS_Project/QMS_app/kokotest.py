from django.utils import  timezone


def update_something():
    print("this function runs every 1 min "+ timezone.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
