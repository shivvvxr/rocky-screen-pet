"""Offline regression tests. Never send prompts to a real provider."""
import json
import sys
import time
import unittest
from unittest.mock import patch

from PySide6.QtCore import QRect, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from rocky_windows.app import RockyWindow
from rocky_windows.session import AgentSession

APP = QApplication.instance() or QApplication([])
APP.setQuitOnLastWindowClosed(False)


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.session = AgentSession()
        self.lines = []
        self.completed = []
        self.session.output.connect(lambda text, kind: self.lines.append((text, kind)))
        self.session.completed.connect(lambda: self.completed.append(True))

    def tearDown(self):
        self.session.stop()

    def wait_idle(self):
        deadline = time.monotonic() + 5
        while self.session.running and time.monotonic() < deadline:
            APP.processEvents()
            time.sleep(.005)
        self.assertFalse(self.session.running)

    def test_process_stream_and_utf8_tail(self):
        self.session.provider = 'codex'
        event = json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message', 'text': 'Hello 🌍'}}, ensure_ascii=False)
        script = 'import sys,time; sys.stdin.buffer.read(); data=' + repr(event.encode('utf-8')) + '; sys.stdout.buffer.write(data[:-3]); sys.stdout.buffer.flush(); time.sleep(.05); sys.stdout.buffer.write(data[-3:])'
        with patch('rocky_windows.session.find_cli', return_value=[sys.executable, '-c', script]):
            self.assertTrue(self.session.send('test & | % prompt'))
            self.wait_idle()
        self.assertIn(('codex: Hello 🌍', 'text'), self.lines)
        self.assertEqual(len(self.completed), 1)

    def test_failure_does_not_celebrate(self):
        self.session.provider = 'codex'
        with patch('rocky_windows.session.find_cli', return_value=[sys.executable, '-c', 'import sys; sys.exit(3)']):
            self.session.send('test')
            self.wait_idle()
        self.assertFalse(self.completed)
        self.assertTrue(any(kind == 'error' for _, kind in self.lines))

    def test_cancel_and_missing_cli(self):
        with patch('rocky_windows.session.find_cli', return_value=[sys.executable, '-c', 'import time; time.sleep(10)']):
            self.session.send('test')
            self.session.stop()
        self.assertFalse(self.session.running)
        self.assertIsNone(self.session.process)
        self.assertFalse(self.completed)
        with patch('rocky_windows.session.find_cli', return_value=None):
            self.assertFalse(self.session.send('test'))
        self.assertFalse(self.session.running)

    def test_claude_session_and_errors(self):
        self.session.provider = 'claude'
        self.session.parse(json.dumps({'type': 'system', 'subtype': 'init', 'session_id': 'test-session'}))
        self.session.parse(json.dumps({'type': 'assistant', 'message': {'content': [
            {'type': 'text', 'text': 'hello'}, {'type': 'tool_use', 'name': 'Read', 'input': {'path': 'x'}}]}}))
        self.assertEqual(self.session.thread_id, 'test-session')
        self.assertIn(('claude: hello', 'text'), self.lines)
        self.assertTrue(any(kind == 'tool' for _, kind in self.lines))
        self.session.parse(json.dumps({'type': 'result', 'is_error': True, 'errors': ['denied']}))
        self.assertTrue(self.session.failed)


class MovementTests(unittest.TestCase):
    def test_negative_monitor_edges_and_jumps(self):
        rocky = RockyWindow()
        rocky.timer.stop()
        rocky.animation.stop()
        try:
            rocky.bounds = QRect(-1280, 0, 1280, 720)
            left, top, right, bottom = rocky.limits()
            for clockwise in (True, False):
                rocky.clockwise = clockwise
                rocky.xpos, rocky.ypos, rocky.wall = -640, bottom, 'bottom'
                walls = set()
                for _ in range(500):
                    rocky.walk(.1)
                    walls.add(rocky.wall)
                    self.assertTrue(left <= rocky.xpos <= right)
                    self.assertTrue(top <= rocky.ypos <= bottom)
                self.assertEqual(walls, {'bottom', 'left', 'right', 'top'})
            rocky.xpos, rocky.ypos, rocky.wall = -640, bottom, 'bottom'
            rocky.jump()
            self.assertTrue(rocky.airborne)
            for _ in range(600):
                rocky.fly(.016)
                if not rocky.airborne:
                    break
            self.assertFalse(rocky.airborne)
            rocky.toggle_chat()
            APP.processEvents()
            self.assertTrue(rocky.chat.isVisible())
            rocky.chat.close()
            self.assertFalse(rocky.chat.isVisible())
        finally:
            rocky.session.stop()
            rocky.tray.hide()
            rocky.chat.hide()
            rocky.hide()
            rocky.deleteLater()


class SettingsTests(unittest.TestCase):
    def test_settings_button_keeps_event_loop_alive_and_recovers(self):
        rocky = RockyWindow()
        try:
            rocky.toggle_chat()
            APP.processEvents()
            QTest.mouseClick(rocky.chat.settings_button, Qt.MouseButton.LeftButton)
            APP.processEvents()
            dialog = rocky.chat.settings_dialog
            self.assertIsNotNone(dialog)
            self.assertTrue(dialog.isVisible())
            self.assertIsNone(APP.activeModalWidget())
            self.assertFalse(dialog.isWindow())
            self.assertIs(dialog.parentWidget(), rocky.chat)
            self.assertTrue(rocky.chat.rect().contains(dialog.geometry()))
            before = rocky.frame
            QTest.qWait(400)
            self.assertGreater(rocky.frame, before)
            rocky.chat.open_settings()
            self.assertIs(rocky.chat.settings_dialog, dialog)
            QTest.keyClick(dialog, Qt.Key.Key_Escape)
            APP.processEvents()
            self.assertIsNone(rocky.chat.settings_dialog)
            self.assertTrue(rocky.chat.settings_button.isEnabled())
            rocky.session.set_running(True)
            QTest.mouseClick(rocky.chat.settings_button, Qt.MouseButton.LeftButton)
            APP.processEvents()
            self.assertTrue(rocky.chat.settings_dialog.isVisible())
            self.assertFalse(rocky.chat.settings_dialog.model.isEnabled())
            rocky.session.set_running(False)
            self.assertTrue(rocky.chat.settings_dialog.model.isEnabled())
        finally:
            if rocky.chat.settings_dialog:
                rocky.chat.settings_dialog.reject()
            rocky.session.stop()
            rocky.chat.hide()
            rocky.tray.hide()
            rocky.hide()
            rocky.deleteLater()


if __name__ == '__main__':
    unittest.main()
