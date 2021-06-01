from .auth import LogoutResource, SignupResource, LoginResource
from .classroom.views import ClassroomsResource, ClassroomResource
from .tasks.views import TasksResource, TaskResource

def initialize_routes(api):
    # Authentication Service
    api.add_resource(SignupResource, '/account/register')
    api.add_resource(LoginResource, '/account/login')
    api.add_resource(LogoutResource, '/account/logout')

    # Class Service
    api.add_resource(ClassroomsResource, '/classes')
    api.add_resource(ClassroomResource, '/classes/<int:id>')
    api.add_resource(TasksResource, '/classes/<int:class_id>/tasks')
    api.add_resource(TaskResource, '/classes/<int:class_id>/tasks/<int:index>')
