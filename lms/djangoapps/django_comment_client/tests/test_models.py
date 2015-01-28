"""
Tests for the django comment client integration models
"""
from django.test.testcases import TestCase
from django.test.utils import override_settings
from opaque_keys.edx.locations import SlashSeparatedCourseKey

from xmodule.modulestore.tests.django_utils import TEST_DATA_MIXED_TOY_MODULESTORE
import django_comment_common.models as models
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase


@override_settings(MODULESTORE=TEST_DATA_MIXED_TOY_MODULESTORE)
class RoleClassTestCase(ModuleStoreTestCase):
    """
    Tests for roles of the comment client service integration
    """
    def setUp(self):
        super(RoleClassTestCase, self).setUp()

        # For course ID, syntax edx/classname/classdate is important
        # because xmodel.course_module.id_to_location looks for a string to split

        self.course_id = SlashSeparatedCourseKey("edX", "toy", "2012_Fall")
        self.student_role = models.Role.objects.get_or_create(name="Student",
                                                              course_id=self.course_id)[0]
        self.student_role.add_permission("delete_thread")
        self.student_2_role = models.Role.objects.get_or_create(name="Student",
                                                                course_id=self.course_id)[0]
        self.TA_role = models.Role.objects.get_or_create(name="Community TA",
                                                         course_id=self.course_id)[0]
        self.course_id_2 = SlashSeparatedCourseKey("edx", "6.002x", "2012_Fall")
        self.TA_role_2 = models.Role.objects.get_or_create(name="Community TA",
                                                           course_id=self.course_id_2)[0]

        class Dummy():
            def render_template():
                pass

    def test_has_permission(self):
        # Whenever you add a permission to student_role,
        # Roles with the same FORUM_ROLE in same class also receives the same
        # permission.
        # Is this desirable behavior?
        self.assertTrue(self.student_role.has_permission("delete_thread"))
        self.assertTrue(self.student_2_role.has_permission("delete_thread"))
        self.assertFalse(self.TA_role.has_permission("delete_thread"))

    def test_inherit_permission(self):
        self.TA_role.inherit_permissions(self.student_role)
        self.assertTrue(self.TA_role.has_permission("delete_thread"))
        # Despite being from 2 different courses, TA_role_2 can still inherit
        # permissions from TA_role without error
        self.TA_role_2.inherit_permissions(self.TA_role)


class PermissionClassTestCase(TestCase):
    """
    Tests for permissions of the comment client service integration
    """
    def setUp(self):
        super(PermissionClassTestCase, self).setUp()
        self.permission = models.Permission.objects.get_or_create(name="test")[0]

    def test_unicode(self):
        self.assertEqual(str(self.permission), "test")
