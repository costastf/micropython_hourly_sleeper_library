# -*- coding: utf-8 -*-
# Micropython code to deep sleep a wemos d1 in multiple increments of hours
# Copyright (C) 2017  Costas Tyfoxylos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import machine
import esp


class HourlySleeper(object):
    def __init__(self, hours):
        rtc = machine.RTC()
        self.memory = rtc.memory
        self.hours = int(hours)

    def _check_reset_cause(self):
        if machine.reset_cause() == machine.HARD_RESET:
            print('Hard reset identified, clearing real time memory')
            self.memory('')

    @property
    def _initialized(self):
        return False if not self.memory() else True

    @property
    def iteration(self):
        return int(self.memory().decode('utf-8'))

    @iteration.setter
    def iteration(self, value):
        self.memory(str(value))

    def _sleep(self):
        if locals().get('HOURLY_SLEEP_DEBUG'):
            print('Debug set, sleeping for 6 seconds instead of an hour')
            duration = 6
        else:
            duration = 60 * 60
        print('Sleeping for hour {} of {}'.format(self.iteration,
                                                  self.hours))
        esp.deepsleep(1000000 * duration)

    def _check(self):
        self._check_reset_cause()
        if not self._initialized:
            self.iteration = 0
        elif self.iteration == self.hours:
            self.memory('')
            self._sleep()
        else:
            self.iteration += 1
            self._sleep()

    def __call__(self, *args, **kwargs):
        self._check()
