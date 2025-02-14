import random


class ReplicationRouter:
    """
    A router to control database operations in a master-slave
    replication set up.
    """

    route_app_labels = {
        "knox",
        "admin",
        "auth",
        "contenttypes",
        "sessions",
        "app",
    }
    primary_alias = "default"
    replica_alias = "replica"

    def db_for_read(self, model, **hints):
        """
        Attempts to read for models in supported apps are distributed
        between the primary and replica databases.
        """
        if model._meta.app_label in self.route_app_labels:
            return random.choice([self.primary_alias, self.replica_alias])
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write for models in supported apps are always
        passed to the primary database.
        """
        if model._meta.app_label in self.route_app_labels:
            return self.primary_alias
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if the models are in the supported apps.
        """
        obj1_valid = obj1._meta.app_label in self.route_app_labels
        obj2_valid = obj2._meta.app_label in self.route_app_labels

        if obj1_valid or obj2_valid:
            return obj1_valid and obj2_valid
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Allow migrations for models in the supported apps only in
        the primary database. No migrations should be applied to the
        replication database, as migrations will be automatically
        replicated.
        """
        if db.startswith(self.replica_alias):
            return False

        if app_label in self.route_app_labels:
            return db == self.primary_alias
        else:
            return False if db == self.primary_alias else None
