"""
keyword_substitution.py

Contains utility functions to help substitute keywords in a text body with
the appropriate user / course data.

Supported:
    LMS:
        - %%USER_ID%% => anonymous user id
        - %%USER_FULLNAME%% => User's full name
        - %%COURSE_DISPLAY_NAME%% => display name of the course
        - %%COURSE_END_DATE%% => end date of the course

Usage:
    KEYWORD_FUNCTION_MAP must be supplied in startup.py, so that it lives
    above other modules in the dependency tree and acts like a global var.
    Then we can call substitute_keywords_with_data where substitution is
    needed. Currently called in:
        - LMS: Announcements + Bulk emails
        - CMS: Not called
"""

from django.contrib.auth.models import User
from student.models import anonymous_id_for_user
from xmodule.modulestore.django import modulestore


def anonymous_id_from_user_id(user_id):
    """
    Gets a user's anonymous id from their user id
    """
    user = User.objects.get(id=user_id)
    return anonymous_id_for_user(user, None)


def substitute_keywords(string, user_id, context):
    """
    Replaces all %%-encoded words using KEYWORD_FUNCTION_MAP mapping functions

    Iterates through all keywords that must be substituted and replaces
    them by calling the corresponding functions stored in KEYWORD_FUNCTION_MAP.

    Functions stored in KEYWORD_FUNCTION_MAP must return a replacement string.
    Also, functions imported from other modules must be wrapped in a
    new function if they don't take in user_id and course_id. This simplifies
    the loop below, and reduces the need for piling up if elif else statements
    when the keyword pool grows.
    """

    # do this lazily to avoid unneeded database hits
    KEYWORD_FUNCTION_MAP = {
        '%%USER_ID%%': lambda: anonymous_id_from_user_id(user_id),
        '%%USER_FULLNAME%%': lambda: context['name'],
        '%%COURSE_DISPLAY_NAME%%': lambda: context['course_title'],
        '%%COURSE_END_DATE%%': lambda: context.get('course_end_date'),
    }

    for key in KEYWORD_FUNCTION_MAP.keys():
        if key in string:
            substitutor = KEYWORD_FUNCTION_MAP[key]
            string = string.replace(key, substitutor())

    return string


def substitute_keywords_with_data(string, context):
    """
    Given user and course ids, replaces all %%-encoded words in the given string
    """

    # Do not proceed without parameters: Compatibility check with existing tests
    # that do not supply these parameters
    user_id = context.get('user_id')
    course_title = context.get('course_title')

    if user_id is None or course_title is None:
        return string

    course_id = context.get('course_id')

    return substitute_keywords(string, user_id, context)
