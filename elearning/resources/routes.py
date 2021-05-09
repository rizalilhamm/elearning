from .auth import SignupApi, LoginApi

def initialize_routes(api):
    api.add_resource(SignupApi, '/account/register')
    api.add_resource(LoginApi, '/account/login')
