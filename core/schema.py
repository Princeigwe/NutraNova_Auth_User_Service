from ariadne import QueryType, make_executable_schema, load_schema_from_path, MutationType
from users import resolvers


type_defs = load_schema_from_path('schemas')

query = QueryType()
# query.set_field("users", resolvers.resolve_users)
# query.set_field("onboardUser", resolvers.resolve_onboardUser)


mutation = MutationType()
mutation.set_field("onboardUser", resolvers.resolve_onboardUser)
mutation.set_field("updateProfile", resolvers.resolve_updateProfile)
mutation.set_field("updateUsername", resolvers.resolve_updateUsername)



schema = make_executable_schema(type_defs, query, mutation, convert_names_case=True)