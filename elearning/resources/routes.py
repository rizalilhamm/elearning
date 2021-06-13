from .auth import LogoutResource, SignupResource, LoginResource
from .classroom import ClassroomsResource, ClassroomResource, TheoryResource
from .tasks import TasksResource, TaskResource
from .participants import ParticipantsResource, ParticipantResource
from .answers import AnswersResource, AnswerResource

def initialize_routes(api):
    # Authentication Service
    api.add_resource(SignupResource, '/account/register')
    api.add_resource(LoginResource, '/account/login')
    api.add_resource(LogoutResource, '/account/logout')

    # Class Service
    api.add_resource(ClassroomsResource, '/classes')
    api.add_resource(ClassroomResource, '/classes/<int:class_id>')
    api.add_resource(TheoryResource, '/classes/<int:class_id>/new_material')
    
    # Task service
    api.add_resource(TasksResource, '/classes/<int:class_id>/tasks')
    api.add_resource(TaskResource, '/classes/<int:class_id>/tasks/<int:index>')

    # Class Participants
    api.add_resource(ParticipantsResource, '/classes/<int:class_id>/participants')
    api.add_resource(ParticipantResource, '/classes/<int:class_id>/participants/<int:index>')
    
    # take result
    api.add_resource(AnswersResource, '/classes/<int:class_id>/tasks/<int:task_id>/answers')
    api.add_resource(AnswerResource, '/classes/<int:class_id>/tasks/<int:task_id>/answers/<int:index>')