#
#     Kwola is an AI algorithm that learns how to use other programs
#     automatically so that it can find bugs in them.
#
#     Copyright (C) 2020 Kwola Software Testing Inc.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from ...config.logger import getLogger
from ...components.proxy.RewriteProxy import RewriteProxy
from ...components.proxy.PathTracer import PathTracer
from .WebEnvironmentSession import WebEnvironmentSession
from contextlib import closing
from mitmproxy.tools.dump import DumpMaster
from threading import Thread
import asyncio
import concurrent.futures
from datetime import datetime
import numpy as np
import socket
import time
import os
from ..plugins.core.RecordAllPaths import RecordAllPaths
from ..plugins.core.RecordBranchTrace import RecordBranchTrace
from ..plugins.core.RecordCursorAtAction import RecordCursorAtAction
from ..plugins.core.RecordExceptions import RecordExceptions
from ..plugins.core.RecordLogEntriesAndLogErrors import RecordLogEntriesAndLogErrors
from ..plugins.core.RecordNetworkErrors import RecordNetworkErrors
from ..plugins.core.RecordPageURLs import RecordPageURLs
from ..plugins.core.RecordScreenshots import RecordScreenshots


class WebEnvironment:
    """
        This class represents web / browser based environments. It will boot up a headless browser and use it to communicate
        with the software.
    """

    def __init__(self, config, sessionLimit=None, plugins=None, executionSessions=None):
        self.config = config

        defaultPlugins = [
            RecordCursorAtAction(),
            RecordExceptions(),
            RecordLogEntriesAndLogErrors(),
            RecordNetworkErrors(),
            RecordPageURLs(),
            RecordAllPaths(),
            RecordBranchTrace(),
            RecordScreenshots()
        ]

        if plugins is None:
            # Put in the default set up plugins
            self.plugins = defaultPlugins
        else:
            self.plugins = defaultPlugins + plugins

        def createSession(number):
            maxAttempts = 10
            for attempt in range(maxAttempts):
                try:
                    return WebEnvironmentSession(config, number, self.plugins, self.executionSessions[number])
                except Exception as e:
                    if attempt == (maxAttempts - 1):
                        raise

        with concurrent.futures.ThreadPoolExecutor(max_workers=config['web_session_max_startup_workers']) as executor:
            sessionCount = config['web_session_parallel_execution_sessions']
            if sessionLimit is not None:
                sessionCount = min(sessionLimit, sessionCount)

            if executionSessions is None:
                self.executionSessions = [None] * sessionCount
            else:
                self.executionSessions = executionSessions

            getLogger().info(f"[{os.getpid()}] Starting up {sessionCount} parallel browser sessions.")

            sessionFutures = [
                executor.submit(createSession, sessionNumber) for sessionNumber in range(sessionCount)
            ]

            self.sessions = [
                future.result() for future in sessionFutures
            ]

    def shutdown(self):
        for session in self.sessions:
            session.shutdown()


    def screenshotSize(self):
        return self.sessions[0].screenshotSize()

    def getImages(self):
        imageFutures = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for session in self.sessions:
                resultFuture = executor.submit(session.getImage)
                imageFutures.append(resultFuture)

        images = [
            imageFuture.result() for imageFuture in imageFutures
        ]
        return images

    def getActionMaps(self):
        actionMapFutures = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for session in self.sessions:
                resultFuture = executor.submit(session.getActionMaps)
                actionMapFutures.append(resultFuture)

        actionMaps = [
            imageFuture.result() for imageFuture in actionMapFutures
        ]
        return actionMaps

    def numberParallelSessions(self):
        return len(self.sessions)

    def runActions(self, actions):
        """
            Run a single action on each of the browser tabs within this environment.

            :param actions:
            :return:
        """

        resultFutures = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            for tab, action in zip(self.sessions, actions):
                resultFuture = executor.submit(tab.runAction, action)
                resultFutures.append(resultFuture)

        results = [
            resultFuture.result() for resultFuture in resultFutures
        ]
        return results

    def removeBadSessionIfNeeded(self):
        """
            This method checks all the browser sessions to see if there are any bad ones. If so, it will remove
            the first bad one it finds and return the index of that session

            :return: None if all sessions are good, integer of the first bad session removed if there was a bad session
                    removed.
        """

        for sessionN, session in enumerate(self.sessions):
            if session.hasBrowserDied:
                del self.sessions[sessionN]
                return sessionN
        return None


    def runSessionCompletedHooks(self):
        for tab in self.sessions:
            tab.runSessionCompletedHooks()

