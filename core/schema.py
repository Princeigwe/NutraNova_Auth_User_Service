from ariadne import QueryType, make_executable_schema, load_schema_from_path, MutationType, ObjectType
from users import resolvers


type_defs = load_schema_from_path('schemas')

query = QueryType()
query.set_field("getUser", resolvers.resolve_get_user)
query.set_field("myFollowers", resolvers.resolve_my_followers)
query.set_field("myFollowing", resolvers.resolve_my_following)
query.set_field("userFollowers", resolvers.resolver_user_followers)
query.set_field("userFollowing", resolvers.resolve_user_following)


mutation = MutationType()
mutation.set_field("onboardUser", resolvers.resolve_onboard_user)
mutation.set_field("updateProfile", resolvers.resolve_update_profile)
mutation.set_field("updateUsername", resolvers.resolve_update_username)
mutation.set_field("followUser", resolvers.resolve_follow_user)


user = ObjectType('User')
user.set_field('password', resolvers.resolve_password_with_permission_check)
user.set_field('medicalConditions', resolvers.resolve_medical_conditions_with_permission_check)


schema = make_executable_schema(type_defs, query, mutation, user, convert_names_case=True)