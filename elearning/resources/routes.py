from .auth import LogoutResource, SignupResource, LoginResource
from .classroom import ClassroomsResource, ClassroomResource
from .tasks import TasksResource, TaskResource
from .participants import ParticipantsResource, ParticipantResource

def initialize_routes(api):
    # Authentication Service
    api.add_resource(SignupResource, '/account/register')
    api.add_resource(LoginResource, '/account/login')
    api.add_resource(LogoutResource, '/account/logout')

    # Class Service
    api.add_resource(ClassroomsResource, '/classes')
    api.add_resource(ClassroomResource, '/classes/<int:class_id>')
    
    # Task service
    api.add_resource(TasksResource, '/classes/<int:class_id>/tasks')
    api.add_resource(TaskResource, '/classes/<int:class_id>/tasks/<int:index>')

    # Class Participants
    api.add_resource(ParticipantsResource, '/classes/<int:class_id>/participants')
    api.add_resource(ParticipantResource, '/classes/<int:class_id>/participants/<int:index>')