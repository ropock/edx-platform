from opaque_keys.edx.keys import CourseKey
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from verify_student.models import VerificationCheckpoint, VerificationStatus


class ReverificationService(object):

    def get_status(self, user_id, course_id, checkpoint_name):
        course_key = CourseKey.from_string(course_id)
        try:
            checkpoint_status = VerificationStatus.objects.filter(
                user_id=user_id,
                checkpoint__course_id=course_key,
                checkpoint__checkpoint_name=checkpoint_name
            ).latest()
            return checkpoint_status.status
        except ObjectDoesNotExist:
            return None

    def start_verification(self, course_id, checkpoint_name, item_id):
        course_key = CourseKey.from_string(course_id)
        VerificationCheckpoint.objects.get_or_create(course_id=course_key, checkpoint_name=checkpoint_name)
        re_verification_link = reverse("verify_student_incourse_reverify", args=(course_id, checkpoint_name))
        return re_verification_link