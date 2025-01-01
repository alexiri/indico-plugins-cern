# This file is part of the CERN Indico plugins.
# Copyright (C) 2014 - 2025 CERN
#
# The CERN Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from datetime import timedelta

import icalendar

from indico.web.http_api import HTTPAPIHook
from indico.web.http_api.util import get_query_parameter

from indico_vc_assistance.definition import VCAssistanceRequest
from indico_vc_assistance.util import (find_requests, get_vc_capable_rooms, is_vc_support,
                                       start_time_within_working_hours)


class VCAssistanceExportHook(HTTPAPIHook):
    TYPES = (VCAssistanceRequest.name,)
    RE = ''
    DEFAULT_DETAIL = 'default'
    MAX_RECORDS = {'default': 100}
    GUEST_ALLOWED = False
    VALID_FORMATS = ('json', 'jsonp', 'xml', 'ics')

    def _getParams(self):
        super()._getParams()
        self._alarm = get_query_parameter(self._queryParams, ['alarms'], None, True)

    def _has_access(self, user):
        return is_vc_support(user)

    @property
    def serializer_args(self):
        return {'ical_serializer': _ical_serialize_vc}

    def export_vc_assistance(self, user):
        results = find_requests(from_dt=self._fromDT, to_dt=self._toDT, contribs_and_sessions=False)
        for req in results:
            yield _serialize_obj(req, self._alarm)


def _serialize_obj(req, alarm):
    # Util to serialize an event in the context of a vc assistance request
    event = req.event
    url = event.external_url
    title = event.title
    unique_id = f'e{event.id}'

    data = {
        'event_id': req.event_id,
        'startDate': event.start_dt,
        'endDate': event.end_dt,
        'title': title,
        'location': event.venue_name or None,
        'room': event.get_room_name(full=False) or None,
        'room_full_name': event.get_room_name(full=True) or None,
        'url': url,
        'comment': req.data['comment'],
        'vc_capable_room': event.room is not None and event.room in get_vc_capable_rooms(),
        'OWH': not start_time_within_working_hours(event),
        '_ical_id': f'indico-vc-assistance-{unique_id}@cern.ch'
    }
    if alarm:
        data['_ical_alarm'] = alarm
    return data


def _ical_serialize_vc(cal, record, now):
    event = icalendar.Event()
    event.add('uid', record['_ical_id'])
    event.add('dtstamp', now)
    event.add('dtstart', record['startDate'])
    event.add('dtend', record['endDate'])
    event.add('url', record['url'])
    event.add('categories', ['Videoconference assistance'])
    event.add('summary', _ical_summary(record))
    location = ': '.join(_f for _f in (record['location'], record['room_full_name']) if _f)
    event.add('location', location)
    description = ['URL: {}'.format(record['url'])]
    if record['comment']:
        description.append('Comment: {}'.format(record['comment']))
    if not record['vc_capable_room']:
        description.append('(!) Room does not have vc capabilities')
    if record['OWH']:
        description.append('(!) Event starts out of working hours')
    event.add('description', '\n'.join(description))
    if '_ical_alarm' in record:
        event.add_component(_ical_serialize_vc_alarm(record))
    cal.add_component(event)


def _ical_summary(record):
    return '{}{} - {}'.format('(!) ' if not record['vc_capable_room'] or record['OWH'] else '',
                              'VC Assistance', record['title'])


def _ical_serialize_vc_alarm(record):
    alarm = icalendar.Alarm()
    alarm.add('trigger', timedelta(minutes=-int(record['_ical_alarm'])))
    alarm.add('action', 'DISPLAY')
    alarm.add('summary', _ical_summary(record))
    alarm.add('description', str(record['url']))
    return alarm
