from .models import CustomUser

# def resolve_createUser(*_, input: dict):
#   clean_input = {
#     "first_name": input["first_name"], 
#     "last_name": input["last_name"], 
#     "email": input["email"], 
#     "username": input["username"],
#     "password": input["password"], 
#   }
#   try:
#     user = User.objects.create(first_name=clean_input["first_name"], last_name=clean_input["last_name"], email=clean_input["email"], username=clean_input["username"], password=clean_input["password"])
#     user.save()
#     return {
#       "message": "User Created",
#       "user": user
#     }
#   except ValueError as error:
#     return {
#       "error": str(error)
#     }


# def resolve_users(*_):
#   users = User.objects.all()
#   return {
#     "message": "Registered Users",
#     "users": users
#   }