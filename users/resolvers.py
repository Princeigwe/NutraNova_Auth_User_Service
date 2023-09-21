from .models import User

def resolve_createUser(*_, first_name: str, last_name: str, email: str, username: str, password: str):
  try:
    user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
    user.save()
    return {
      "message": "User Created",
      "user": user
    }
  except ValueError as error:
    return {
      "error": str(error)
    }


def resolve_users(*_):
  users = User.objects.all()
  return {
    "message": "Registered Users",
    "users": users
  }