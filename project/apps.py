from django.apps import AppConfig


class ProjectConfig(AppConfig):
    name = 'project'

    verbose_name = 'Project'

    def ready(self):
        import project.signal
