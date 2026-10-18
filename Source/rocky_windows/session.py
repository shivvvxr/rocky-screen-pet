"""Nonblocking CLI sessions; all signals are delivered on Qt's UI thread."""
import json
import os
from pathlib import Path
import shutil
import subprocess

from PySide6.QtCore import QObject, QProcess, QProcessEnvironment, Signal


def find_cli(provider):
    """Resolve native executables or npm JS entrypoints without invoking a shell."""
    home = Path.home()
    found = shutil.which(provider + '.exe') or shutil.which(provider)
    if found and Path(found).suffix.lower() not in ('.cmd', '.bat', '.ps1'):
        return [found]
    for directory in (home / '.local/bin', home / '.cargo/bin',
                      home / 'AppData/Local/Microsoft/WinGet/Links'):
        candidate = directory / (provider + '.exe')
        if candidate.is_file():
            return [str(candidate)]
    node = shutil.which('node')
    roots = [Path(os.environ.get('APPDATA', str(home))) / 'npm',
             home / '.npm-global', Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'nodejs']
    if found:
        roots.insert(0, Path(found).parent)
    relative = ('@anthropic-ai/claude-code/cli.js' if provider == 'claude'
                else '@openai/codex/bin/codex.js')
    if node:
        for root in roots:
            entry = root / 'node_modules' / relative
            if entry.is_file():
                return [node, str(entry)]
    return None


class AgentSession(QObject):
    output = Signal(str, str)
    running_changed = Signal(bool)
    completed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.provider = 'codex' if find_cli('codex') else 'claude'
        self.model = ''
        self.effort = 'high'
        self.cwd = str(Path.home())
        self.full_access = False
        self.process = None
        self.running = False
        self.history = []
        self.thread_id = None
        self.buffer = bytearray()
        self.error_buffer = bytearray()
        self.failed = False

    def set_running(self, value):
        if self.running != value:
            self.running = value
            self.running_changed.emit(value)

    def reset(self):
        self.stop()
        self.history.clear()
        self.thread_id = None
        self.output.emit('New conversation. Working folder: ' + self.cwd, 'system')

    def stop(self):
        proc, self.process = self.process, None
        if proc:
            proc.blockSignals(True)
            if proc.state() != QProcess.ProcessState.NotRunning:
                if os.name == 'nt' and proc.processId():
                    # npm CLIs and agent tools spawn descendants. Stop the whole tree.
                    subprocess.run(['taskkill', '/PID', str(proc.processId()), '/T', '/F'],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW, check=False)
                proc.kill()
                proc.waitForFinished(3000)
            proc.deleteLater()
        self.set_running(False)

    def send(self, prompt):
        if self.running or not prompt.strip():
            return False
        command = find_cli(self.provider)
        if not command:
            self.output.emit(f'{self.provider} CLI not found. Install it and sign in, then try again.', 'error')
            return False
        if not Path(self.cwd).is_dir():
            self.output.emit('The working folder no longer exists. Choose a folder in Settings.', 'error')
            return False
        self.buffer.clear()
        self.error_buffer.clear()
        self.failed = False
        if self.provider == 'claude':
            args = ['-p', '--output-format', 'stream-json', '--input-format', 'stream-json', '--verbose']
            args += ['--dangerously-skip-permissions'] if self.full_access else ['--permission-mode', 'dontAsk']
            if self.thread_id:
                args += ['--resume', self.thread_id]
            if self.model.strip():
                args += ['--model', self.model.strip()]
            if self.effort:
                args += ['--effort', self.effort]
            payload = json.dumps({'type': 'user', 'message': {'role': 'user', 'content': prompt}}) + '\n'
        else:
            args = ([] if self.full_access else ['-a', 'never']) + ['exec', '--json', '--skip-git-repo-check', '-C', self.cwd]
            args += (['--dangerously-bypass-approvals-and-sandbox'] if self.full_access
                     else ['--sandbox', 'workspace-write'])
            if self.model.strip():
                args += ['-m', self.model.strip()]
            if self.effort:
                args += ['-c', f'model_reasoning_effort="{self.effort}"']
            args += ['-']
            prior = self.history[-12:]
            payload = (('Continue this conversation.\n\n' + '\n\n'.join(
                f'{role}: {text}' for role, text in prior) + '\n\nLatest user message:\n') if prior else '') + prompt
        proc = QProcess(self)
        proc.setWorkingDirectory(self.cwd)
        env = QProcessEnvironment.systemEnvironment()
        env.remove('CLAUDECODE')
        env.remove('CLAUDE_CODE_ENTRYPOINT')
        proc.setProcessEnvironment(env)
        proc.readyReadStandardOutput.connect(self.read_stdout)
        proc.readyReadStandardError.connect(self.read_stderr)
        proc.finished.connect(self.finished)
        proc.errorOccurred.connect(self.process_error)
        proc.started.connect(lambda: (proc.write(payload.encode('utf-8')), proc.closeWriteChannel()))
        self.process = proc
        self.history.append(('user', prompt))
        self.history = self.history[-40:]
        self.output.emit('you: ' + prompt, 'user')
        self.set_running(True)
        proc.start(command[0], command[1:] + args)
        return True

    def process_error(self, error):
        if error == QProcess.ProcessError.FailedToStart:
            self.output.emit('Could not start agent: ' + self.process.errorString(), 'error')
            self.failed = True
            self.stop()

    def read_stdout(self):
        if not self.process:
            return
        self.buffer.extend(bytes(self.process.readAllStandardOutput()))
        while b'\n' in self.buffer:
            line, _, rest = self.buffer.partition(b'\n')
            self.buffer = bytearray(rest)
            self.parse(line.decode('utf-8', errors='replace'))

    def read_stderr(self):
        if not self.process:
            return
        self.error_buffer.extend(bytes(self.process.readAllStandardError()))
        while b'\n' in self.error_buffer:
            line, _, rest = self.error_buffer.partition(b'\n')
            self.error_buffer = bytearray(rest)
            if line.strip():
                self.output.emit(line.decode('utf-8', errors='replace'), 'system')

    def assistant(self, text):
        if text.strip():
            self.history.append(('assistant', text))
            self.history = self.history[-40:]
            self.output.emit(self.provider + ': ' + text, 'text')

    def parse(self, raw):
        if not raw.strip():
            return
        try:
            event = json.loads(raw)
        except (ValueError, TypeError):
            self.output.emit(raw, 'system')
            return
        if not isinstance(event, dict):
            return
        kind = event.get('type', '')
        if self.provider == 'claude':
            if event.get('session_id'):
                self.thread_id = event['session_id']
            if kind == 'assistant':
                for block in event.get('message', {}).get('content', []):
                    if block.get('type') == 'text':
                        self.assistant(block.get('text', ''))
                    elif block.get('type') == 'tool_use':
                        self.output.emit('[' + block.get('name', 'tool') + '] ' + json.dumps(block.get('input', {}), ensure_ascii=False), 'tool')
            elif kind == 'result' and event.get('is_error'):
                self.failed = True
                self.output.emit(event.get('result') or '\n'.join(event.get('errors', [])) or 'Claude task failed.', 'error')
        else:
            item = event.get('item') or {}
            if kind == 'item.completed' and item.get('type') == 'agent_message':
                self.assistant(item.get('text', ''))
            elif kind in ('item.started', 'item.completed') and item.get('type') in ('command_execution', 'file_change', 'mcp_tool_call', 'web_search'):
                detail = item.get('command') or item.get('changes') or item.get('tool') or item.get('query', '')
                self.output.emit(f"[{item['type']}] {detail}", 'tool')
            elif kind in ('error', 'turn.failed'):
                self.failed = True
                detail = event.get('message') or event.get('error', {}).get('message') or raw
                self.output.emit(str(detail), 'error')

    def finished(self, code, status):
        self.read_stdout()
        self.read_stderr()
        if self.buffer:
            self.parse(self.buffer.decode('utf-8', errors='replace'))
            self.buffer.clear()
        if self.error_buffer:
            self.output.emit(self.error_buffer.decode('utf-8', errors='replace'), 'system')
            self.error_buffer.clear()
        success = code == 0 and not self.failed
        self.output.emit('Task complete.' if success else f'Agent stopped (exit {code}).', 'system' if success else 'error')
        proc, self.process = self.process, None
        if proc:
            proc.deleteLater()
        self.set_running(False)
        if success:
            self.completed.emit()
