from __future__ import absolute_import
import json
from functools import partial
from os import path

from iktomi.cms.item_lock.redis import RedisItemLock as ItemLock
from iktomi.utils import quote_js
from iktomi.utils.storage import (
    storage_method,
    storage_cached_property,
)

import ikcms.apps.composite.env
from ikcms.utils import cached_property
from ikcms.web import Response

class Environment(ikcms.apps.composite.env.Environment):

    def render_to_response(self, *args, **kwargs):
        return self.render.to_response(*args, **kwargs)

    @storage_method
    def json(self, data):
        if getattr(self, '_flash', None):
            assert '_flashmessages' not in data
            data = dict(data, _flashmessages=self._flash)
        return Response(
            json.dumps(data),
            content_type="application/json",
            charset='utf8',
        )

    @cached_property
    def cfg(self):
        return self.app.cfg

    @cached_property
    def streams(self):
        return self.app.streams

    @storage_cached_property
    def url_for(storage):
        return storage.root.build_url

    def url_for_static(self, part):
        while part.startswith('/'):
            part = part[1:]
        return path.join(self.cfg.STATIC_URL, part)

    def render_to_string(self, template_name, context):
        return self.render.render(template_name, **context)

    @cached_property
    def render_to_response(self):
        return self.render.to_response

    @cached_property
    def template(self):
        return self.render

    @cached_property
    def context(self):
        return self.Context(self)

    #@storage_cached_property
    #def user(storage):
    #    return storage.user

    @cached_property
    def models(self):
        class Models(object):
            admin = self.app.db.get_models('admin')
            front = self.app.db.get_models('front')
        return Models()

    @storage_cached_property
    def redis(storage):
        return storage.app.cache.client

    @cached_property
    def auth_model(self):
        return self.models.admin.AdminUser

    @storage_cached_property
    def item_lock(storage):
        return ItemLock(storage)

    @storage_cached_property
    def lang(storage):
        return storage.app.i18n.Lang(storage.app.i18n, 'ru')

    @storage_cached_property
    def gettext(self):
        return self.lang.gettext

    @storage_cached_property
    def ngettext(self):
        return self.lang.ngettext

    @storage_method
    def get_template_vars(self):
        d = dict(
            context=self.app.get_context(self),
            user=getattr(self, 'user', None),
            quote_js=quote_js,
            url_for=self.url_for,
            url_for_static=self.url_for_static,
            packed_js_tag=partial(self.app.packer.js_tag, self),
            packed_css_tag=partial(self.app.packer.css_tag, self),
        )
        import_settings = getattr(self.cfg, 'TEMPLATE_IMPORT_SETTINGS', [])
        for key in import_settings:
            d[key] = getattr(self.cfg, key)
        return d

    @storage_cached_property
    def _lang(storage):
        lang = getattr(storage, 'lang', 'ru')
        return storage.app.i18n.langs[lang]

    @storage_cached_property
    def gettext(storage):
        return storage._lang.gettext

    @storage_cached_property
    def ngettext(storage):
        return storage._lang.ngettext

    # XXX: Copypasted from iktomi-cms Environment
    # override this method with configured HelpLoader.get_help to be able
    # to use help messages in admin
    def get_help(self, *args, **kwargs):
        return ''

