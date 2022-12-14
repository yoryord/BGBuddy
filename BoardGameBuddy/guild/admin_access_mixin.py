from django.http import Http404


class AdminAccessMixin:
    """Verify that the current user is admin to a guild."""
    request = None
    model = None

    def admin_check(self, context):
        admins = context["object"].admins.all()
        if self.request.user.buddyprofile not in admins:
            raise Http404("Wrong way")
