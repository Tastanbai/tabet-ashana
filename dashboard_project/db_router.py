class AuthRouter:
    """
    Направляет все запросы Django Auth и ContentTypes в `db1`
    """

    def db_for_read(self, model, **hints):
        """Читаем из db1 только таблицы аутентификации"""
        if model._meta.app_label in ['auth', 'contenttypes']:
            return 'db1'
        return None

    def db_for_write(self, model, **hints):
        """Записываем в db1 только таблицы аутентификации"""
        if model._meta.app_label in ['auth', 'contenttypes']:
            return 'db1'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Мигрируем auth и contenttypes только в db1"""
        if app_label in ['auth', 'contenttypes']:
            return db == 'db1'
        return False
