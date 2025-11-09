from typing import cast

from textual import on
from textual import getters
from textual.app import ComposeResult

from textual.screen import ModalScreen
from textual import containers
from textual import widgets
from textual.reactive import var

import toad
from toad.agent_schema import Action, Agent, OS, Command
from toad.app import ToadApp


class AgentModal(ModalScreen):
    AUTO_FOCUS = "#launcher-checkbox"

    BINDINGS = [("escape", "dismiss", "Dismiss")]

    action = var("")

    app = getters.app(ToadApp)

    def __init__(self, agent: Agent) -> None:
        self._agent = agent
        super().__init__()

    def compose(self) -> ComposeResult:
        launcher_set = frozenset(
            self.app.settings.get("launcher.agents", str).splitlines()
        )

        agent = self._agent

        actions = agent["actions"]

        script_os = cast(OS, toad.os)
        if script_os not in actions:
            script_os = "*"

        commands: dict[Action, Command] = actions[cast(OS, script_os)]
        script_choices = [
            (action["description"], name) for name, action in commands.items()
        ]

        with containers.Vertical(id="container"):
            with containers.VerticalScroll(id="description-container"):
                yield widgets.Markdown(agent["help"], id="description")
            with containers.VerticalGroup():
                with containers.HorizontalGroup():
                    yield widgets.Checkbox(
                        "Show in launcher",
                        value=agent["identity"] in launcher_set,
                        id="launcher-checkbox",
                    )
                    yield widgets.Select(
                        script_choices,
                        prompt="Actions",
                        allow_blank=True,
                        id="script-select",
                    )
                    yield widgets.Button(
                        "Go", variant="primary", id="run-action", disabled=True
                    )

    @on(widgets.Checkbox.Changed)
    def on_checkbox_changed(self, event: widgets.Select.Changed) -> None:
        launcher_set = set(self.app.settings.get("launcher.agents", str).splitlines())
        agent_identity = self._agent["identity"]
        if event.value:
            launcher_set.add(agent_identity)
        else:
            launcher_set.discard(agent_identity)
        self.app.settings.set("launcher.agents", "\n".join(launcher_set))

    @on(widgets.Select.Changed)
    def on_select_changed(self, event: widgets.Select.Changed) -> None:
        self.action = event.value if isinstance(event.value, str) else ""

    def watch_action(self, action: str) -> None:
        go_button = self.query_one("#run-action", widgets.Button)
        go_button.disabled = not action
