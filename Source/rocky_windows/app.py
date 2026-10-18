"""Transparent Windows companion, animation, chat, settings and system tray."""
import argparse
import math
from pathlib import Path
import random
import sys
import time

from PySide6.QtCore import QPoint, QRectF, QSettings, Qt, QTimer, Signal, QEvent
from PySide6.QtGui import QColor, QCursor, QFont, QIcon, QPainter, QPen, QPixmap, QTextCharFormat, QTextCursor, QTextBlockFormat, QShortcut, QKeySequence, QLinearGradient, QPainterPath, QPalette
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QDialogButtonBox, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMenu, QMessageBox, QPushButton, QSystemTrayIcon, QTextEdit, QPlainTextEdit, QFrame, QVBoxLayout, QWidget, QSizeGrip, QScrollArea)

from .session import AgentSession


def asset_root():
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent)) / 'agentrocky'


STYLE = '''
QWidget { background: transparent; color: #c9e7ed; font: 11px Consolas; }
QWidget#settings { background: #0b1721; border: 1px solid #397f99; }
QFrame#header { background: rgba(8, 39, 54, 125); border-bottom: 1px solid rgba(75, 210, 240, 100); }
QLabel { background: transparent; }
QLabel#eyebrow { color: #edbc71; font: bold 9px Consolas; }
QLabel#title { color: #b9f5ff; font: bold 20px Consolas; }
QLabel#subtitle, QLabel#hint { color: #93b8c6; font: 9px Consolas; }
QLabel#badge { color: #8eecff; background: rgba(20, 94, 114, 90); border: 1px solid #32758a;
              border-radius: 3px; padding: 4px 7px; font: bold 9px Consolas; }
QLabel#badge[busy="true"] { color: #edc27e; background: #342a1b; border-color: #635030; }
QLabel#workspace { color: #87c9dd; font: 10px Consolas; }
QTextEdit { background: transparent; border: 0; padding: 5px; selection-background-color: #245971; font: 12px Consolas; }
QFrame#composer { background: rgba(9, 44, 63, 160); border: 1px solid #397f99; border-radius: 4px; }
QPlainTextEdit { background: transparent; color: #e2f8ff; border: 0; padding: 3px; font: 12px Consolas; }
QLabel#prompt { color: #74e9ff; font: bold 17px Consolas; }
QLineEdit, QComboBox { background: #102c3a; color: #e3f6ff; border: 1px solid #30667b; border-radius: 4px; padding: 8px; }
QComboBox QAbstractItemView { background: #102c3a; color: #e3f6ff; selection-background-color: #245971; }
QPushButton { background: rgba(11, 46, 63, 145); color: #b6e7f5; border: 1px solid #30667b; border-radius: 3px; padding: 6px 9px; }
QPushButton:hover { background: rgba(28, 100, 127, 170); color: #effcff; border-color: #77e8ff; }
QPushButton:disabled { color: #4d635d; border-color: #1c2c2c; }
QPushButton#send { color: #061d2b; background: #7de7ff; border: 1px solid #c4f7ff; font-weight: bold; padding: 8px 12px; }
QPushButton#send:hover { background: #b7f4ff; }
QPushButton#send:disabled { background: #173d50; color: #7398aa; border-color: #30667b; }
QPushButton#stop { color: #e99c92; }
QScrollBar:vertical { background: #0b1014; width: 7px; margin: 0; }
QScrollBar::handle:vertical { background: #304b46; min-height: 25px; border-radius: 3px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: #0b1014; }
QCheckBox { spacing: 8px; }
QPushButton#windowControl { background: transparent; color: #82bbcc; border: 0; padding: 1px; font: 16px Consolas; }
QPushButton#windowControl:hover { color: #eac07d; background: rgba(68, 125, 146, 70); }
'''

IDLE_MESSAGES = (
    'amaze amaze amaze',
    'fist my bump',
    'rocky do big science',
    'you and rocky got this',
    'rocky ready!',
)


class SettingsPanel(QWidget):
    finished = Signal(int)

    def __init__(self, rocky):
        super().__init__(rocky.chat)
        self.setObjectName('settings')
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(12, 12, 12, 12)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        fields = QWidget()
        form = QFormLayout(fields)
        form.setContentsMargins(4, 4, 4, 4)
        form.setVerticalSpacing(12)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        scroll.setWidget(fields)
        outer.addWidget(scroll, 1)
        title = QLabel('Agent settings')
        title.setObjectName('title')
        form.addRow(title)
        self.provider = QComboBox()
        self.provider.addItems(['codex', 'claude'])
        self.provider.setCurrentText(rocky.session.provider)
        self.model = QLineEdit(rocky.session.model)
        self.model.setPlaceholderText('Use the CLI default model')
        self.effort = QComboBox()
        self.effort.addItems(['', 'low', 'medium', 'high', 'xhigh', 'max'])
        self.effort.setCurrentText(rocky.session.effort)
        self.folder = QLineEdit(rocky.session.cwd)
        folder_row = QHBoxLayout()
        folder_row.addWidget(self.folder)
        browse = QPushButton('Browse…')
        browse.clicked.connect(self.browse)
        folder_row.addWidget(browse)
        self.full = QCheckBox('Allow full computer access (skip approvals)')
        self.full.setChecked(rocky.session.full_access)
        self.full.setToolTip('Enables the original app’s unrestricted agent execution mode.')
        form.addRow('Backend', self.provider)
        form.addRow('Model', self.model)
        form.addRow('Thinking', self.effort)
        form.addRow('Working folder', folder_row)
        form.addRow(self.full)
        hint = QLabel('Sign in to your chosen CLI in a terminal before chatting.\nChanging settings starts a new conversation.')
        hint.setWordWrap(True)
        form.addRow(hint)
        self.error = QLabel()
        self.error.setWordWrap(True)
        self.error.setStyleSheet('color: #ff9d8f; border: 0;')
        form.addRow(self.error)
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.save)
        self.buttons.rejected.connect(self.reject)
        outer.addWidget(self.buttons)
        self.rocky = rocky
        self.edit_controls = [self.provider, self.model, self.effort, self.folder, browse, self.full]
        rocky.session.running_changed.connect(self.set_busy)
        self.set_busy(rocky.session.running)

    def set_busy(self, running):
        for control in self.edit_controls:
            control.setEnabled(not running)
        self.buttons.button(QDialogButtonBox.StandardButton.Save).setEnabled(not running)
        self.error.setText('A task is running. Close Settings and stop the task to make changes.' if running else '')

    def reject(self):
        self.hide()
        self.finished.emit(0)

    def accept(self):
        self.hide()
        self.finished.emit(1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

    def browse(self):
        folder = QFileDialog.getExistingDirectory(self, 'Agent working folder', self.folder.text())
        if folder:
            self.folder.setText(folder)

    def save(self):
        if self.rocky.session.running:
            return
        if not Path(self.folder.text()).is_dir():
            self.error.setText('Choose an existing working folder.')
            return
        session = self.rocky.session
        session.provider = self.provider.currentText()
        session.model = self.model.text().strip()
        session.effort = self.effort.currentText()
        session.cwd = self.folder.text()
        session.full_access = self.full.isChecked()
        for key in ('provider', 'model', 'effort', 'cwd', 'full_access'):
            self.rocky.settings.setValue(key, getattr(session, key))
        session.reset()
        self.rocky.chat.update_status()
        self.accept()


class PromptInput(QPlainTextEdit):
    submitted = Signal()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.submitted.emit()
        else:
            super().keyPressEvent(event)


class ChatWindow(QWidget):
    def __init__(self, rocky):
        super().__init__(None, Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setObjectName('terminal')
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.rocky = rocky
        self.settings_dialog = None
        self.setWindowTitle('Rocky Terminal')
        self.setWindowIcon(rocky.icon)
        self.setStyleSheet(STYLE)
        self.resize(500, 550)
        self.setMinimumSize(460, 440)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 12)
        layout.setSpacing(8)
        header = QFrame()
        header.setObjectName('header')
        head = QHBoxLayout(header)
        head.setContentsMargins(10, 12, 10, 12)
        portrait = QLabel()
        portrait.setPixmap(rocky.frames['stand'].scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        head.addWidget(portrait)
        titles = QVBoxLayout()
        titles.setSpacing(2)
        eyebrow = QLabel('R / 01  ·  COMPANION INTERFACE')
        eyebrow.setObjectName('eyebrow')
        title = QLabel('ROCKY TERMINAL')
        title.setObjectName('title')
        subtitle = QLabel('NEURAL LINK / COMMAND TERMINAL')
        subtitle.setObjectName('subtitle')
        for label in (eyebrow, title, subtitle):
            titles.addWidget(label)
        head.addLayout(titles, 1)
        self.badge = QLabel('● READY')
        self.badge.setObjectName('badge')
        controls = QVBoxLayout()
        controls.setSpacing(7)
        window_buttons = QHBoxLayout()
        window_buttons.addStretch()
        for text, tooltip, callback in [('−', 'Minimize terminal', self.showMinimized), ('×', 'Hide terminal', self.close)]:
            button = QPushButton(text)
            button.setObjectName('windowControl')
            button.setFixedSize(22, 20)
            button.setToolTip(tooltip)
            button.clicked.connect(callback)
            window_buttons.addWidget(button)
        controls.addLayout(window_buttons)
        controls.addWidget(self.badge)
        head.addLayout(controls)
        for drag_surface in (header, portrait, eyebrow, title, subtitle):
            drag_surface.installEventFilter(self)
            drag_surface.setCursor(Qt.CursorShape.SizeAllCursor)
        layout.addWidget(header)
        tools = QWidget()
        bar = QHBoxLayout()
        bar.setContentsMargins(18, 0, 18, 0)
        tools.setLayout(bar)
        self.settings_button = QPushButton('Settings')
        self.settings_button.clicked.connect(self.open_settings)
        self.new_button = QPushButton('New chat')
        self.new_button.clicked.connect(self.new_chat)
        self.stop_button = QPushButton('Stop')
        self.stop_button.setObjectName('stop')
        self.stop_button.clicked.connect(self.stop)
        for button in (self.settings_button, self.new_button, self.stop_button):
            bar.addWidget(button)
        bar.addStretch()
        copy_button = QPushButton('Copy log')
        copy_button.setToolTip('Copy the selected output, or the entire log')
        copy_button.clicked.connect(self.copy_log)
        bar.addWidget(copy_button)
        layout.addWidget(tools)
        self.status = QLabel()
        self.status.setObjectName('workspace')
        self.status.setContentsMargins(20, 0, 20, 0)
        layout.addWidget(self.status)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.document().setMaximumBlockCount(6000)
        self.output.setContentsMargins(12, 0, 12, 0)
        layout.addWidget(self.output, 1)
        self.entry_count = 0
        self.started_at = None
        composer_wrap = QHBoxLayout()
        composer_wrap.setContentsMargins(18, 0, 18, 0)
        composer = QFrame()
        composer.setObjectName('composer')
        row = QHBoxLayout(composer)
        row.setContentsMargins(12, 10, 12, 10)
        prompt = QLabel('❯')
        prompt.setObjectName('prompt')
        row.addWidget(prompt, 0, Qt.AlignmentFlag.AlignTop)
        self.input = PromptInput()
        self.input.setFixedHeight(48)
        self.input.setPlaceholderText('What are we building today?')
        self.input.submitted.connect(self.send)
        row.addWidget(self.input, 1)
        self.send_button = QPushButton('Send ↵')
        self.send_button.setObjectName('send')
        self.send_button.clicked.connect(self.send)
        row.addWidget(self.send_button)
        composer_wrap.addWidget(composer)
        layout.addLayout(composer_wrap)
        footer = QHBoxLayout()
        footer.setContentsMargins(20, 0, 20, 0)
        hint = QLabel('ENTER send · SHIFT+ENTER new line')
        hint.setObjectName('hint')
        footer.addWidget(hint)
        footer.addStretch()
        self.activity = QLabel('READY')
        self.activity.setObjectName('hint')
        footer.addWidget(self.activity)
        grip = QSizeGrip(self)
        grip.setFixedSize(14, 14)
        grip.setToolTip('Resize terminal')
        footer.addWidget(grip)
        layout.addLayout(footer)
        for editor in (self.output, self.input):
            editor.viewport().setAutoFillBackground(False)
            palette = editor.palette()
            palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0, 0))
            editor.setPalette(palette)
        self.activity_timer = QTimer(self)
        self.activity_timer.timeout.connect(self.update_activity)
        self.activity_timer.start(1000)
        self.shortcuts = []
        for key, action in [('Ctrl+L', self.clear_log), ('Ctrl+N', self.new_chat), ('Ctrl+Shift+C', self.copy_log)]:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(action)
            self.shortcuts.append(shortcut)
        rocky.session.output.connect(self.append)
        rocky.session.running_changed.connect(self.running_changed)
        self.running_changed(False)

    def append(self, text, kind):
        if kind == 'system':
            return
        colors = {'text': '#c9eff7', 'tool': '#69e0ff', 'error': '#ff9d8f', 'system': '#92b8c9', 'user': '#f3cb87'}
        cursor = self.output.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if not self.output.document().isEmpty():
            cursor.insertBlock()
        block = QTextBlockFormat()
        block.setTopMargin(8)
        block.setBottomMargin(4)
        block.setLeftMargin(8)
        cursor.setBlockFormat(block)
        label = QTextCharFormat()
        label.setForeground(QColor(colors.get(kind, '#b6e9cc')))
        label.setFontPointSize(9)
        label.setFontWeight(QFont.Weight.Bold)
        names = {'text': 'ROCKY', 'user': 'YOU', 'tool': 'TOOL', 'error': 'ERROR'}
        cursor.insertText(f'{names.get(kind, "LOG")}  /  {time.strftime("%H:%M")}\n', label)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(colors.get(kind, '#80efab')))
        fmt.setFontPointSize(10)
        if kind == 'user' and text.startswith('you: '):
            text = text[5:]
        elif kind == 'text' and text.startswith(self.rocky.session.provider + ': '):
            text = text[len(self.rocky.session.provider) + 2:]
        cursor.insertText(text + '\n', fmt)
        self.output.setTextCursor(cursor)
        self.output.ensureCursorVisible()
        self.entry_count += 1
        self.update_activity()

    def update_status(self):
        s = self.rocky.session
        folder = Path(s.cwd).name or s.cwd
        self.status.setText(f'ROCKY  /  {s.model or "default model"}  /  {folder}')
        self.status.setToolTip(s.cwd)
        self.badge.setText('● WORKING' if s.running else '● READY')
        self.badge.setProperty('busy', s.running)
        self.badge.style().unpolish(self.badge)
        self.badge.style().polish(self.badge)

    def update_activity(self):
        if self.started_at is not None:
            elapsed = int(time.monotonic() - self.started_at)
            self.activity.setText(f'RUNNING {elapsed // 60:02d}:{elapsed % 60:02d}')
        else:
            self.activity.setText(f'{self.entry_count:03d} LOG ENTRIES')

    def clear_log(self):
        self.output.clear()
        self.entry_count = 0
        self.update_activity()

    def copy_log(self):
        cursor = self.output.textCursor()
        QApplication.clipboard().setText(cursor.selectedText().replace('\u2029', '\n') if cursor.hasSelection() else self.output.toPlainText())

    def running_changed(self, running):
        self.started_at = time.monotonic() if running else None
        for control in (self.new_button, self.send_button, self.input):
            control.setEnabled(not running)
        self.stop_button.setEnabled(running)
        self.update_status()
        self.update_activity()
        if not running:
            self.input.setFocus()

    def send(self):
        if self.rocky.session.send(self.input.toPlainText().strip()):
            self.input.clear()

    def stop(self):
        self.rocky.session.stop()
        # Claude's interrupted resume state and the local transcript may differ.
        self.rocky.session.thread_id = None
        self.append('Task stopped. Start a new chat to clear the transcript.', 'system')

    def new_chat(self):
        if self.rocky.session.running:
            return
        self.clear_log()
        self.rocky.session.reset()

    def open_settings(self):
        if self.settings_dialog is None:
            self.settings_dialog = SettingsPanel(self.rocky)
            self.settings_dialog.finished.connect(self.settings_closed)
        self.settings_dialog.setGeometry(self.rect().adjusted(12, 92, -12, -16))
        self.settings_dialog.show()
        self.settings_dialog.raise_()
        self.settings_dialog.provider.setFocus()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.settings_dialog:
            self.settings_dialog.setGeometry(self.rect().adjusted(12, 92, -12, -16))

    def settings_closed(self, result):
        dialog, self.settings_dialog = self.settings_dialog, None
        if dialog:
            dialog.deleteLater()
        self.raise_()
        self.activateWindow()
        self.input.setFocus()

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            handle = self.windowHandle()
            if handle and handle.startSystemMove():
                return True
        return super().eventFilter(watched, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width() - 1, self.height() - 1
        shape = QPainterPath()
        shape.moveTo(16, 0)
        shape.lineTo(w - 30, 0)
        shape.lineTo(w, 30)
        shape.lineTo(w, h - 16)
        shape.lineTo(w - 16, h)
        shape.lineTo(0, h)
        shape.lineTo(0, 16)
        shape.closeSubpath()
        glass = QLinearGradient(0, 0, w, h)
        glass.setColorAt(0, QColor(5, 26, 42, 212))
        glass.setColorAt(1, QColor(3, 15, 27, 182))
        painter.fillPath(shape, glass)
        painter.setPen(QPen(QColor(95, 217, 248, 150), 1))
        painter.drawPath(shape)
        painter.save()
        painter.setClipPath(shape)
        painter.setPen(QColor(99, 220, 255, 9))
        for y in range(110, h - 115, 5):
            painter.drawLine(10, y, w - 10, y)
        painter.restore()
        painter.setPen(QPen(QColor('#83e8ff'), 2))
        painter.drawLine(20, 1, 76, 1)
        painter.drawLine(1, 24, 1, 64)
        painter.drawLine(w - 1, h - 65, w - 1, h - 24)
        painter.setPen(QPen(QColor('#edbc71'), 2))
        painter.drawLine(w - 94, h - 1, w - 34, h - 1)
        painter.end()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.settings_dialog:
                self.settings_dialog.reject()
            else:
                self.hide()
        else:
            super().keyPressEvent(event)


class RockyWindow(QWidget):
    def __init__(self):
        super().__init__(None, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFixedSize(180, 160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip('Click to chat · Drag to move · Right-click for controls')
        self.frames = {name: QPixmap(str(asset_root() / (name + '.png'))) for name in
                       ['stand', 'walkleft1', 'walkleft2', 'jazz1', 'jazz2', 'jazz3']}
        if any(frame.isNull() for frame in self.frames.values()):
            raise RuntimeError('Missing sprite images. Keep the agentrocky asset folder with the app.')
        self.icon = QIcon(self.frames['stand'])
        self.setWindowIcon(self.icon)
        self.settings = QSettings('AgentRocky', 'RockyWindows')
        self.session = AgentSession(self)
        for key in ('provider', 'model', 'effort', 'cwd'):
            value = self.settings.value(key)
            if value is not None:
                setattr(self.session, key, str(value))
        self.session.full_access = self.settings.value('full_access', False, type=bool)
        if self.session.provider not in ('codex', 'claude'):
            self.session.provider = 'codex'
        self.chat = ChatWindow(self)
        self.session.running_changed.connect(self.task_state)
        self.session.completed.connect(self.celebrate)
        self.wall = 'bottom'
        self.clockwise = random.choice([True, False])
        self.facing = 1
        self.sleeping = False
        self.dragging = False
        self.press_point = None
        self.airborne = False
        self.parachute = False
        self.high_jump = False
        self.vx = self.vy = 0.0
        self.speed = 100.0
        self.jazz_until = self.look_until = 0.0
        self.antic = None
        self.antic_started = self.antic_until = 0.0
        self.last_antic = None
        self.next_antic = 0.0
        self.bubble = ''
        self.bubble_until = 0.0
        self.last_idle_message = None
        self.frame = 0
        self.bounds = QApplication.primaryScreen().availableGeometry()
        self.xpos = self.bounds.center().x() - self.width() / 2
        self.ypos = self.bounds.bottom() - self.height() + 1
        self.move(round(self.xpos), round(self.ypos))
        self.last_tick = time.monotonic()
        self.next_decision = self.last_tick + 4
        self.next_jump = self.last_tick + random.uniform(8, 18)
        self.next_jazz = self.last_tick + random.uniform(3, 6)
        self.next_look = self.last_tick + random.uniform(5, 9)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(16)
        self.animation = QTimer(self)
        self.animation.timeout.connect(self.animate)
        self.animation.start(125)
        self.tray = QSystemTrayIcon(self.icon, self)
        self.tray.setToolTip('Rocky · Desktop companion')
        self.tray.setContextMenu(self.make_menu())
        self.tray.activated.connect(self.tray_activated)
        self.tray.messageClicked.connect(self.toggle_chat)
        self.tray.show()
        for screen in QApplication.screens():
            screen.availableGeometryChanged.connect(self.screen_changed)
        QApplication.instance().screenRemoved.connect(self.screen_changed)

    def make_menu(self):
        menu = QMenu(self)
        menu.addAction('Open chat', self.toggle_chat)
        self.sleep_action = menu.addAction('Sleep / Wake', self.toggle_sleep)
        menu.addAction('Jump', self.jump)
        menu.addAction('Dance', lambda: self.dance(3))
        menu.addAction('Bring Rocky back', self.bring_back)
        menu.addSeparator()
        menu.addAction('Quit Rocky', QApplication.instance().quit)
        return menu

    def tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_chat()

    def screen_changed(self, *_):
        screen = QApplication.screenAt(self.geometry().center()) or QApplication.primaryScreen()
        self.bounds = screen.availableGeometry()
        self.snap()

    def bring_back(self):
        self.bounds = QApplication.primaryScreen().availableGeometry()
        self.wall = 'bottom'
        self.xpos = self.bounds.center().x() - self.width() / 2
        self.ypos = self.bounds.bottom() - self.height() + 1
        self.snap()
        self.show()

    def limits(self):
        b = self.bounds
        return b.left(), b.top(), b.right() - self.width() + 1, b.bottom() - self.height() + 1

    def snap(self):
        left, top, right, bottom = self.limits()
        self.xpos = min(max(self.xpos, left), right)
        self.ypos = min(max(self.ypos, top), bottom)
        distances = {'left': abs(self.xpos-left), 'right': abs(self.xpos-right),
                     'top': abs(self.ypos-top), 'bottom': abs(self.ypos-bottom)}
        self.wall = min(distances, key=distances.get)
        if self.wall == 'left': self.xpos = left
        if self.wall == 'right': self.xpos = right
        if self.wall == 'top': self.ypos = top
        if self.wall == 'bottom': self.ypos = bottom
        self.airborne = self.parachute = False
        self.move(round(self.xpos), round(self.ypos))

    def toggle_chat(self):
        if self.chat.isVisible() and not self.chat.isMinimized():
            self.chat.hide()
            return
        self.sleeping = False
        self.airborne = False
        self.snap()
        bounds = self.bounds
        x = min(max(self.x() - 150, bounds.left()), max(bounds.left(), bounds.right() - self.chat.width() + 1))
        y = self.y() - self.chat.height() - 8
        y = min(max(y, bounds.top()), max(bounds.top(), bounds.bottom() - self.chat.height() + 1))
        self.chat.move(x, y)
        self.chat.showNormal()
        self.chat.raise_()
        self.chat.activateWindow()
        self.chat.input.setFocus()
        self.next_antic = time.monotonic() + random.uniform(1, 2)

    def toggle_sleep(self):
        self.sleeping = not self.sleeping
        self.snap()
        self.jazz_until = 0
        self.antic = None
        self.antic_until = 0
        self.say('zzz' if self.sleeping else 'awake', 2)

    def say(self, text, duration=3):
        self.bubble = text
        self.bubble_until = time.monotonic() + duration
        self.update()

    def task_state(self, running):
        if running:
            self.sleeping = False
            self.say(random.choice(['working', 'building', 'thinking']), 86400)
        else:
            self.bubble_until = 0

    def dance(self, duration, message=None):
        if not self.sleeping and not self.airborne:
            self.antic = None
            self.antic_until = 0
            self.jazz_until = time.monotonic() + duration
            message = message or random.choice([text for text in IDLE_MESSAGES if text != self.last_idle_message])
            self.last_idle_message = message
            self.say(message, duration)

    def chat_antics(self, now):
        if (self.sleeping or self.dragging or self.airborne or now < self.next_antic
                or now < self.jazz_until or now < self.antic_until):
            return
        choices = ['dance', 'bounce', 'spin', 'peek', 'wiggle']
        kind = random.choice([choice for choice in choices if choice != self.last_antic])
        self.last_antic = kind
        duration = random.uniform(2.4, 3.4)
        if kind == 'dance':
            self.dance(duration)
        else:
            self.antic = kind
            self.antic_started = now
            self.antic_until = now + duration
            self.say({'bounce': 'rocky got hops', 'spin': 'maximum science',
                      'peek': 'what you building?', 'wiggle': 'fist my bump'}[kind], duration)
        self.next_antic = now + duration + random.uniform(3, 7)

    def celebrate(self):
        self.dance(3, random.choice(['rocky done!', 'fist my bump', 'amaze amaze amaze']))
        if not self.chat.isVisible():
            self.tray.showMessage('Rocky', 'Your agent task is complete.', QSystemTrayIcon.MessageIcon.Information, 4000)

    def jump(self):
        if self.sleeping or self.dragging or self.airborne or self.chat.isVisible():
            return
        self.airborne = True
        self.high_jump = random.random() < .32
        tangent = 1 if self.clockwise else -1
        lift = random.uniform(1.28, 1.48) if self.high_jump else 1
        self.vx, self.vy = {
            'bottom': (tangent * self.speed * 1.2, -420 * lift),
            'top': (-tangent * self.speed * 1.2, 230),
            'left': (273, -220 * lift), 'right': (-273, -220 * lift)
        }[self.wall]
        # Start inside the perimeter so the departure wall does not catch the jump.
        dx, dy = {'bottom': (0, -2), 'top': (0, 2), 'left': (2, 0), 'right': (-2, 0)}[self.wall]
        self.xpos += dx
        self.ypos += dy

    def animate(self):
        self.frame += 1
        self.update()

    def tick(self):
        now = time.monotonic()
        dt = min(now - self.last_tick, .05)
        self.last_tick = now
        chat_open = self.chat.isVisible() and not self.chat.isMinimized()
        if chat_open:
            self.chat_antics(now)
            if not self.sleeping:
                self.update()
        paused = self.sleeping or self.dragging or chat_open
        if not paused and now >= self.jazz_until and now >= self.look_until:
            if self.airborne:
                self.fly(dt)
            else:
                self.walk(dt)
                if now >= self.next_decision:
                    self.next_decision = now + random.uniform(3, 8)
                    if random.random() < .42:
                        self.clockwise = not self.clockwise
                    self.speed = random.uniform(65, 145)
                if now >= self.next_jump:
                    self.next_jump = now + random.uniform(12, 28)
                    self.jump()
                if now >= self.next_jazz:
                    self.next_jazz = now + random.uniform(15, 30)
                    self.dance(2)
                if now >= self.next_look:
                    self.next_look = now + random.uniform(10, 22)
                    self.look_until = now + .6
        self.move(round(self.xpos), round(self.ypos))

    def walk(self, dt):
        left, top, right, bottom = self.limits()
        sign = 1 if self.clockwise else -1
        dx, dy = {'bottom': (sign, 0), 'right': (0, -sign),
                  'top': (-sign, 0), 'left': (0, sign)}[self.wall]
        self.xpos += dx * self.speed * dt
        self.ypos += dy * self.speed * dt
        self.facing = sign
        if self.wall == 'bottom' and (self.xpos >= right or self.xpos <= left):
            self.wall = 'right' if dx > 0 else 'left'
        elif self.wall == 'right' and (self.ypos <= top or self.ypos >= bottom):
            self.wall = 'top' if dy < 0 else 'bottom'
        elif self.wall == 'top' and (self.xpos <= left or self.xpos >= right):
            self.wall = 'left' if dx < 0 else 'right'
        elif self.wall == 'left' and (self.ypos >= bottom or self.ypos <= top):
            self.wall = 'bottom' if dy > 0 else 'top'
        self.xpos = min(max(self.xpos, left), right)
        self.ypos = min(max(self.ypos, top), bottom)

    def fly(self, dt):
        left, top, right, bottom = self.limits()
        self.parachute = self.high_jump and self.vy > 210 and self.ypos < bottom - 180
        self.vy += (260 if self.parachute else 980) * dt
        if self.parachute:
            self.vy = min(self.vy, 150)
            self.vx *= .992
        self.xpos += self.vx * dt
        self.ypos += self.vy * dt
        if self.xpos <= left or self.xpos >= right or self.ypos <= top or self.ypos >= bottom:
            self.snap()

    def paintEvent(self, _):
        now = time.monotonic()
        dancing = now < self.jazz_until
        antic = self.antic if now < self.antic_until else None
        name = ('stand' if self.sleeping else f'jazz{self.frame % 3 + 1}' if dancing
                else f'walkleft{self.frame % 2 + 1}' if antic in ('bounce', 'wiggle')
                else 'stand' if self.chat.isVisible() or now < self.look_until else f'walkleft{self.frame % 2 + 1}')
        pix = self.frames[name]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        # Body placement touches the appropriate work-area edge after rotation.
        cx, cy = {'bottom': (90, 112), 'top': (90, 48), 'left': (48, 80), 'right': (132, 80)}[self.wall]
        if self.airborne:
            cx, cy = 90, 112
        progress = max(0, (now - self.antic_started) / max(.01, self.antic_until - self.antic_started))
        if antic and not self.sleeping:
            inward_x, inward_y = {'bottom': (0, -1), 'top': (0, 1),
                                  'left': (1, 0), 'right': (-1, 0)}[self.wall]
            offset = 5
            if antic == 'bounce':
                offset += abs(math.sin(progress * math.pi * 6)) * 10
            cx += inward_x * offset
            cy += inward_y * offset
        if self.parachute:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            canopy = QPainterPath()
            canopy.moveTo(35, 40)
            canopy.cubicTo(40, -5, 140, -5, 145, 40)
            canopy.quadTo(131, 32, 118, 40)
            canopy.quadTo(104, 32, 90, 40)
            canopy.quadTo(76, 32, 62, 40)
            canopy.quadTo(49, 32, 35, 40)
            canopy.closeSubpath()
            canopy_glass = QLinearGradient(35, 4, 145, 44)
            canopy_glass.setColorAt(0, QColor(5, 26, 42, 235))
            canopy_glass.setColorAt(1, QColor(12, 67, 89, 215))
            painter.fillPath(canopy, canopy_glass)
            painter.setPen(QPen(QColor('#83e8ff'), 1.5))
            painter.drawPath(canopy)
            seams = QPainterPath()
            seams.moveTo(90, 6)
            seams.quadTo(65, 15, 62, 40)
            seams.moveTo(90, 6)
            seams.lineTo(90, 36)
            seams.moveTo(90, 6)
            seams.quadTo(115, 15, 118, 40)
            painter.setPen(QPen(QColor(131, 232, 255, 125), 1))
            painter.drawPath(seams)
            painter.setPen(QPen(QColor('#edbc71'), 2))
            painter.drawLine(81, 7, 99, 7)
            painter.setPen(QPen(QColor('#83e8ff'), 1))
            painter.drawLine(35, 39, 80, 93)
            painter.drawLine(145, 39, 100, 93)
            painter.setPen(QPen(QColor('#edbc71'), 1))
            painter.drawLine(62, 40, 85, 93)
            painter.drawLine(118, 40, 95, 93)
        painter.save()
        painter.translate(cx, cy)
        angle = 0 if self.airborne else {'bottom': 0, 'right': -90, 'top': 180, 'left': 90}[self.wall]
        if now < self.look_until:
            angle += math.sin(now * 15) * 8
        if antic == 'spin':
            angle += 360 * (progress * progress * (3 - 2 * progress))
            painter.scale(.78, .78)
        elif antic == 'wiggle':
            angle += math.sin(progress * math.pi * 10) * 12
            painter.scale(.92, .92)
        elif antic == 'peek':
            angle += math.sin(progress * math.pi * 4) * 10
            painter.scale(.92, .92)
        painter.rotate(angle)
        facing = self.facing
        if antic == 'peek' and int(progress * 4) % 2:
            facing = -facing
        cursor = self.mapFromGlobal(QCursor.pos())
        distance = math.hypot(cursor.x() - cx, cursor.y() - cy)
        if not self.airborne and not self.sleeping and self.wall == 'bottom' and 150 < distance < 280:
            facing = 1 if cursor.x() > cx else -1
        painter.scale(-1 if facing > 0 else 1, 1)
        if self.sleeping:
            painter.scale(1, .96 + .025 * math.sin(now * 2))
        scaled = pix.size().scaled(118, 96, Qt.AspectRatioMode.KeepAspectRatio)
        painter.drawPixmap(-scaled.width() // 2, -scaled.height() // 2, scaled.width(), scaled.height(), pix)
        painter.restore()
        text = ('zzz' if self.sleeping else self.bubble if now < self.bubble_until
                else 'working' if self.session.running else '')
        if text:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setFont(QFont('Consolas', 9, QFont.Weight.Bold))
            bubble_height = 28 if self.sleeping else 44
            bubble_y = self.height() - bubble_height - 4 if self.wall == 'top' and not self.airborne else 4
            bubble = QPainterPath()
            bubble.moveTo(25, bubble_y)
            bubble.lineTo(153, bubble_y)
            bubble.lineTo(163, bubble_y + 10)
            bubble.lineTo(163, bubble_y + bubble_height - 6)
            bubble.lineTo(157, bubble_y + bubble_height)
            bubble.lineTo(17, bubble_y + bubble_height)
            bubble.lineTo(17, bubble_y + 8)
            bubble.closeSubpath()
            glass = QLinearGradient(17, bubble_y, 163, bubble_y + bubble_height)
            glass.setColorAt(0, QColor(5, 26, 42, 225))
            glass.setColorAt(1, QColor(3, 15, 27, 205))
            painter.fillPath(bubble, glass)
            painter.setPen(QPen(QColor('#83e8ff'), 1))
            painter.drawPath(bubble)
            painter.setPen(QPen(QColor('#edbc71'), 2))
            painter.drawLine(29, bubble_y + 1, 53, bubble_y + 1)
            painter.setPen(QColor('#b9f5ff'))
            painter.drawText(QRectF(23, bubble_y + 2, 134, bubble_height - 4),
                             Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap, text)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.press_point = event.globalPosition().toPoint()
            self.drag_origin = self.pos()
            self.dragging = False

    def mouseMoveEvent(self, event):
        if self.press_point is None or not event.buttons() & Qt.MouseButton.LeftButton:
            return
        delta = event.globalPosition().toPoint() - self.press_point
        if delta.manhattanLength() > QApplication.startDragDistance():
            self.dragging = True
        if self.dragging:
            point = self.drag_origin + delta
            self.xpos, self.ypos = point.x(), point.y()
            self.move(point)

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton or self.press_point is None:
            return
        if self.dragging:
            screen = QApplication.screenAt(event.globalPosition().toPoint()) or QApplication.primaryScreen()
            self.bounds = screen.availableGeometry()
            self.snap()
        else:
            self.toggle_chat()
        self.press_point = None
        self.dragging = False

    def contextMenuEvent(self, event):
        self.tray.contextMenu().exec(event.globalPos())


def main():
    parser = argparse.ArgumentParser(description='Rocky desktop companion for Windows')
    parser.add_argument('--smoke-test', action='store_true', help='Exercise animation and chat, then exit without contacting an agent')
    parser.add_argument('--chat', action='store_true', help='Open the terminal on startup')
    args = parser.parse_args()
    app = QApplication(sys.argv[:1])
    app.setApplicationName('Rocky')
    app.setQuitOnLastWindowClosed(False)
    rocky = RockyWindow()
    app.aboutToQuit.connect(rocky.session.stop)
    rocky.show()
    if args.chat:
        rocky.toggle_chat()
    if args.smoke_test:
        def exercise():
            rocky.toggle_chat()
            rocky.chat.append('Smoke test: chat and renderer initialized.', 'system')
            rocky.chat.hide()
            rocky.jump()
        QTimer.singleShot(200, exercise)
        QTimer.singleShot(1800, app.quit)
    return app.exec()
