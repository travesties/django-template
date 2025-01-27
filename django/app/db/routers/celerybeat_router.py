class CeleryBeatRouter:
    """
    A router to control all database operations on models in the
    django_celery_beat application.
    """

    route_app_labels = {"django_celery_beat"}
    db_alias = "celerybeat"

    def db_for_read(self, model, **hints):
        """
        Attempts to read django_celery_beat go to celerybeat.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.db_alias
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write django_celery_beat go to celerybeat.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.db_alias
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the django_celery_beat app is involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return obj1._meta.app_label == obj2._meta.app_label
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the django_celery_beat app only appears in the
        'celerybeat' database.
        """
        if app_label in self.route_app_labels:
            return db == self.db_alias
        return False if db == self.db_alias else None
