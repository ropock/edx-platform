from opaque_keys.edx.keys import CourseKey
from verify_student.models import VerificationCheckpoint


class ReverificationService(object):

    def get_status(self, course_id, checkpoint_name):
        course_key = CourseKey.from_string(course_id)
        checkpoint = VerificationCheckpoint.get_verification_checkpoint(course_key, checkpoint_name)
        checkpoint_status = checkpoint.get_latest_status()
        if checkpoint_status:
            return checkpoint_status.status
        return None

    def start_verification(self, course_id, checkpoint_name, item_id):
        course_key = CourseKey.from_string(course_id)
        VerificationCheckpoint.objects.get_or_create(course_id=course_key, checkpoint_name=checkpoint_name)
        # link = "<a href='/verify_student/reverify/{course_id}/{checkpoint_name}/{item_id}'>Reverify Now</a>"
        # link.format(course_id=course_id, checkpoint_name=checkpoint_name, item_id=item_id)
        # return link
