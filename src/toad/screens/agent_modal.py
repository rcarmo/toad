from typing import cast

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual import containers
from textual import widgets

import toad
from toad.screens.store_schema import Agent, OS


class AgentModal(ModalScreen):
    AUTO_FOCUS = "#script-select"

    BINDINGS = [("escape", "dismiss", "Dismiss")]

    def __init__(self, agent: Agent) -> None:
        self._agent = agent
        super().__init__()

    def compose(self) -> ComposeResult:
        agent = self._agent

        scripts = agent["scripts"]

        script_os = cast(OS, toad.os)
        if script_os not in scripts:
            script_os = "*"

        scripts = scripts[cast(OS, script_os)]
        script_choices = [
            (script["description"], name) for name, script in scripts.items()
        ]

        with containers.Vertical(id="container"):
            with containers.VerticalScroll(id="description-container"):
                yield widgets.Markdown(agent["help"], id="description")
            with containers.VerticalGroup():
                with containers.HorizontalGroup():
                    yield widgets.Select(
                        script_choices, allow_blank=False, id="script-select"
                    )
                    yield widgets.Button("Go", variant="primary")


if __name__ == "__main__":
    from textual.app import App

    AGENT: Agent = {
        "identity": "claude-code.anthropic.ai",
        "name": "Claude Code",
        "type": "acp",
        "short_name": "claude",
        "author_name": "Anthropic",
        "author_url": "https://www.anthropic.com/",
        "publisher_name": "Anthropic",
        "publisher_url": "https://www.anthropic.com/",
        "description": "Claude Code is a command-line tool that lets developers delegate coding tasks to Claude directly from their terminal. It provides agentic coding capabilities with Claude's latest models.",
        "tags": ["coding"],
        "help": '# Claude Code\n\nClaude Code is an AI-powered coding assistant that runs in your terminal.\n\n## Features\n- Direct terminal integration\n- Autonomous coding capabilities\n- File editing and creation\n- Multi-file context awareness\n\n## Usage\n```bash\nclaude "add error handling to auth.py"\n```\n\nFor more information, visit [docs.claude.com](https://docs.claude.com)\n',
        "run_command": {"*": "claude"},
        "scripts": {
            "macos": {
                "install": {
                    "description": "Install Claude Code on macOS",
                    "type": "bash",
                    "script": "curl -fsSL https://claude.ai/install.sh | bash",
                },
                "uninstall": {
                    "description": "Uninstall Claude Code from macOS",
                    "type": "bash",
                    "script": "rm -rf ~/.claude && rm /usr/local/bin/claude",
                },
                "update": {
                    "description": "Update Claude Code to the latest version",
                    "type": "bash",
                    "script": "claude update",
                },
            },
            "linux": {
                "install": {
                    "description": "Install Claude Code on Linux",
                    "type": "bash",
                    "script": "curl -fsSL https://claude.ai/install.sh | bash",
                },
                "uninstall": {
                    "description": "Uninstall Claude Code from Linux",
                    "type": "bash",
                    "script": "rm -rf ~/.claude && sudo rm /usr/local/bin/claude",
                },
                "update": {
                    "description": "Update Claude Code to the latest version",
                    "type": "bash",
                    "script": "claude update",
                },
            },
            "windows": {
                "install": {
                    "description": "Install Claude Code on Windows",
                    "type": "bash",
                    "script": 'powershell -Command "iwr -useb https://claude.ai/install.ps1 | iex"',
                },
                "uninstall": {
                    "description": "Uninstall Claude Code from Windows",
                    "type": "bash",
                    "script": 'powershell -Command "Remove-Item -Recurse -Force $env:USERPROFILE\\.claude"',
                },
                "update": {
                    "description": "Update Claude Code to the latest version",
                    "type": "bash",
                    "script": "claude update",
                },
            },
        },
    }

    class TestApp(App):
        def on_mount(self) -> None:
            self.push_screen(AgentModal(AGENT))

    TestApp().run()
