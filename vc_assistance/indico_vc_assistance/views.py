# This file is part of the CERN Indico plugins.
# Copyright (C) 2014 - 2021 CERN
#
# The CERN Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from indico.core.plugins import WPJinjaMixinPlugin
from indico.web.breadcrumbs import render_breadcrumbs
from indico.web.views import WPDecorated

from indico_audiovisual import _


class WPVCAssistance(WPJinjaMixinPlugin, WPDecorated):
    def _get_breadcrumbs(self):
        return render_breadcrumbs(_('Videoconference assistance'))

    def _get_body(self, params):
        return self._get_page_content(params)
