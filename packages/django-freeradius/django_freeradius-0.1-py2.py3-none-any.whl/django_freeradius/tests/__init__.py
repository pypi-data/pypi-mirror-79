import os

from django.core.management import call_command

from django_freeradius.base.models import _encode_secret


class CreateRadiusObjectsMixin(object):
    def _get_defaults(self, opts, model=None):
        options = {}
        options.update(opts)
        return options

    def _create_radius_check(self, **kwargs):
        if kwargs.get('value'):
            kwargs['value'] = _encode_secret(kwargs['attribute'],
                                             kwargs.get('value'))
        options = self._get_defaults(kwargs)
        rc = self.radius_check_model(**options)
        rc.full_clean()
        rc.save()
        return rc

    def _create_radius_accounting(self, **kwargs):
        options = self._get_defaults(kwargs)
        ra = self.radius_accounting_model(**options)
        ra.full_clean()
        ra.save()
        return ra

    def _create_radius_reply(self, **kwargs):
        options = self._get_defaults(kwargs)
        rr = self.radius_reply_model(**options)
        rr.full_clean()
        rr.save()
        return rr

    def _create_nas(self, **kwargs):
        options = self._get_defaults(kwargs)
        n = self.nas_model(**options)
        n.full_clean()
        n.save()
        return n

    def _create_radius_group(self, **kwargs):
        options = self._get_defaults(kwargs)
        rg = self.radius_group_model(**options)
        rg.full_clean()
        rg.save()
        return rg

    def _create_radius_groupcheck(self, **kwargs):
        options = self._get_defaults(kwargs,
                                     model=self.radius_groupcheck_model)
        c = self.radius_groupcheck_model(**options)
        c.full_clean()
        c.save()
        return c

    def _create_radius_groupreply(self, **kwargs):
        options = self._get_defaults(kwargs,
                                     model=self.radius_groupreply_model)
        r = self.radius_groupreply_model(**options)
        r.full_clean()
        r.save()
        return r

    def _create_radius_usergroup(self, **kwargs):
        options = self._get_defaults(kwargs,
                                     model=self.radius_usergroup_model)
        ug = self.radius_usergroup_model(**options)
        ug.full_clean()
        ug.save()
        return ug

    def _create_radius_postauth(self, **kwargs):
        options = self._get_defaults(kwargs)
        rp = self.radius_postauth_model(**options)
        rp.full_clean()
        rp.save()
        return rp

    def _create_radius_batch(self, **kwargs):
        options = self._get_defaults(kwargs)
        rb = self.radius_batch_model(**options)
        rb.full_clean()
        rb.save()
        return rb

    def _create_user(self, **kwargs):
        u = self.user_model(**kwargs)
        u.set_password(kwargs['password'])
        u.full_clean()
        u.save()
        return u


class PostParamsMixin(object):
    def _get_post_defaults(self, opts, model=None):
        options = {}
        options.update(**opts)
        return options

    def _get_postauth_params(self, **kwargs):
        params = {'username': 'molly',
                  'password': 'barbar',
                  'reply': 'Access-Accept',
                  'called_station_id': '00-11-22-33-44-55:hostname',
                  'calling_station_id': '00:26:b9:20:5f:10'}
        params.update(kwargs)
        return self._get_post_defaults(params)

    def _get_accounting_params(self, **kwargs):
        return self._get_post_defaults(kwargs)


class FileMixin(object):
    def _get_path(self, file):
        d = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(d, file)


class CallCommandMixin(object):
    def _call_command(self, command, **kwargs):
        call_command(command, **kwargs)
