from ariadne import QueryType, make_executable_schema, load_schema_from_path, MutationType, ObjectType
from users import resolvers


type_defs = load_schema_from_path('schemas')

query = QueryType()
query.set_field("getUser", resolvers.resolve_get_user)


mutation = MutationType()
mutation.set_field("onboardUser", resolvers.resolve_onboard_user)
mutation.set_field("updateProfile", resolvers.resolve_update_profile)
mutation.set_field("updateUsername", resolvers.resolve_update_username)


user = ObjectType('User')
user.set_field('password', resolvers.resolve_password_with_permission_check)
user.set_field('medicalConditions', resolvers.resolve_medical_conditions_with_permission_check)


schema = make_executable_schema(type_defs, query, mutation, user, convert_names_case=True)