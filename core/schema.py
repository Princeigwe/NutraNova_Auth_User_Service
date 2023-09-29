from ariadne import QueryType, make_executable_schema, load_schema_from_path, MutationType
from users import resolvers


type_defs = load_schema_from_path('schemas')

query = QueryType()
# query.set_field("users", resolvers.resolve_users)


mutation = MutationType()
# mutation.set_field('createUser', resolvers.resolve_createUser)

schema = make_executable_schema(type_defs, query, mutation)