from .auth import LogoutResource, SignupResource, LoginResource
from .classroom.views import Classroom, classroomSelect

def initialize_routes(api):
    # Authentication Service
    api.add_resource(SignupResource, '/account/register')
    api.add_resource(LoginResource, '/account/login')
    api.add_resource(LogoutResource, '/account/logout')

    # Class Service
    api.add_resource(Classroom, '/classes')
    api.add_resource(classroomSelect, '/classes/<int:id>')