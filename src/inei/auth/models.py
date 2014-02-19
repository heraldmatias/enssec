# -*- coding: utf-8 -*-
__author__ = 'holivares'

from django.db import models
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)


class Usuario(models.Model):
    id = models.AutoField(primary_key=True, db_column='nu_usuario')
    username = models.CharField(max_length=50, unique=True, db_index=True, db_column='co_usuario')
    is_active = models.BooleanField(db_column='fl_activo')
    is_admin = models.BooleanField(db_column='fl_administrador')
    password = models.CharField(max_length=40, db_column='co_clave')
    last_login = models.DateTimeField(blank=True, null=True, db_column='fe_ultimoacceso')
    nombres = models.CharField(max_length=20, db_column='no_nombres')
    apellidoPaterno = models.CharField(max_length=20, db_column='no_apellidopaterno')
    apellidoMaterno = models.CharField(max_length=20, db_column='no_apellidomaterno')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth']

    class Meta:
        db_table = 'usuario'

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return self.get_username()

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    def get_full_name(self):
        # The user is identified by their username address
        return u'%s %s %s' % (self.nombres, self.apellido_paterno, self.apellido_materno)

    def get_short_name(self):
        # The user is identified by their username address
        return self.username

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin