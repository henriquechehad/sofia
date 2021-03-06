from django.views import generic
from django.shortcuts import get_object_or_404

from apps.learn.models import Project, Announcement
from apps.learn.views.mixins import EnrollmentPermissionMixin


class ProjectHomeView(EnrollmentPermissionMixin, generic.ListView):

    template_name = 'learn/internal/project_home.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = self.get_project().announcements.filter(fixed=False)
        tag = self.kwargs.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProjectHomeView, self).get_context_data(**kwargs)
        project = self.get_project()
        context['fixed_announcements'] = project.announcements.filter(
            fixed=True
        )
        return context


class AnnouncementDetailView(EnrollmentPermissionMixin, generic.DetailView):

    template_name = 'learn/internal/announcement.html'
    slug_url_kwarg = 'announcement'
    context_object_name = 'announcement'

    def get_queryset(self):
        return self.get_project().announcements.all()


project_home = ProjectHomeView.as_view()
announcements_tagged = ProjectHomeView.as_view()
announcement_detail = AnnouncementDetailView.as_view()
