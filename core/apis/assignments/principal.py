from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs.exceptions import FyleError
from core.models.assignments import Assignment, AssignmentStateEnum
from flask import jsonify
from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)



@principal_assignments_resources.route('/assignments' , methods = ['GET'] , strict_slashes = False)
#todo : decorator thingy
@decorators.authenticate_principal
def list_assignments(p):
    """Return list of Graded Assignments"""
    graded_assignments = Assignment.get_assignments_by_principal()
    graded_assignments_dump = AssignmentSchema().dump(graded_assignments)
    return APIResponse.respond(data=graded_assignments_dump)

@principal_assignments_resources.route('/assignments/grade' , methods=['POST'] , strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    try:
        # Load and validate incoming payload
        # print(incoming_payload)
        grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

        # Retrieve assignment from database
        assignment = Assignment.query.get(grade_assignment_payload.id)
        if not assignment:
            raise FyleError(404 , "Assignment not found", )

        # Check assignment state
        if assignment.state == AssignmentStateEnum.DRAFT:
            raise FyleError(400, "Assignment in DRAFT state cannot be graded")

        # Mark assignment as graded
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )

        # Commit changes to database
        db.session.commit()

        # Serialize graded assignment to JSON
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

        # Return successful response
        return APIResponse.respond(data=graded_assignment_dump)

    except FyleError as e:
        # Handle specific FyleError exceptions
        return APIResponse.respond_error(message=str(e), status_code=e.status_code)

    # except Exception as e:
    #     # Handle unexpected errors
    #     print('this is the error ' , e)
    #     return APIResponse.respond_error(message='Internal Server Error', status_code=412)
