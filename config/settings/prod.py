from decouple import config
print("dev.py")

SECRET_KEY = config("SECRET_KEY")

DEBUG = False
