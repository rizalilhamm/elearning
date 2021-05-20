from .auth import SignupResource, LoginResource, LogoutResource

def initialize_routes(api):
    api.add_resource(SignupResource, '/account/register')
    api.add_resource(LoginResource, '/account/login')
    api.add_resource(LogoutResource, '/account/logout')
