from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)



@principal_assignments_resources.route('/assignments' , methods = ['GET'] , strict_slashes = False)
def list_assignments():
    """Return list of Graded Assignments"""
    graded_assignments = Assignment.get_assignments_by_principal()
    graded_assignments_dump = AssignmentSchema().dump(graded_assignments)
    return APIResponse.respond(data=graded_assignments_dump)



