from __future__ import annotations

from dataclasses import dataclass

from textual.app import ComposeResult
from textual.binding import Binding
from textual import containers
from textual.content import Content
from textual.reactive import var, reactive
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label


type Questions = list[tuple[str, str]]


class Option(containers.HorizontalGroup):
    DEFAULT_CSS = """
    Option {        
        color: $text-muted;
        #caret {
            visibility: hidden;
            padding: 0 1;
        }
        #index {
            padding-right: 1;
        }
        #label {
            width: 1fr;
        }
        &.-active {
            background: $boost;
            color: $text-accent;
            #caret {
                visibility: visible;
            }
        }
        &.-selected {
            opacity: 0.5;
        }
        &.-active.-selected {
            opacity: 1.0;
            background: transparent;
            color: $text-accent;            
            #label {
                text-style: underline;
            }
            #caret {
                visibility: hidden;
            }
        }
    }
    """

    selected: reactive[bool] = reactive(False, toggle_class="-selected")

    def __init__(self, index: int, content: Content, classes: str = "") -> None:
        super().__init__(classes=classes)
        self.index = index
        self.content = content

    def compose(self) -> ComposeResult:
        yield Label("❯", id="caret")
        yield Label(f"{self.index + 1}.", id="index")
        yield Label(self.content, id="label")


class Question(Widget, can_focus=True):
    BINDINGS = [
        Binding("up", "selection_up", "Up"),
        Binding("down", "selection_down", "Down"),
        Binding("enter", "select", "Select"),
    ]

    DEFAULT_CSS = """
    Question {
        width: 1fr;
        padding: 1; 
        #prompt {
            margin-bottom: 1;
            color: $text-primary;
        }                
    }
    """

    question: var[str] = var("")
    options: var[Questions] = var(list)

    selection: reactive[int] = reactive(0, init=False)
    selected: var[bool] = var(False, toggle_class="-selected")

    @dataclass
    class Response(Message):
        """User selected a response."""

        index: int

    def __init__(
        self,
        question: str,
        options: Questions,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.set_reactive(Question.question, question)
        self.set_reactive(Question.options, options)

    def compose(self) -> ComposeResult:
        with containers.VerticalGroup():
            if self.question:
                yield Label(self.question, id="prompt")
            with containers.VerticalGroup(id="option-container"):
                for index, (option_text, _option_id) in enumerate(self.options):
                    active = index == self.selection
                    yield Option(
                        index, Content(option_text), classes="-active" if active else ""
                    ).data_bind(Question.selected)

    def watch_selection(self, old_selection: int, new_selection: int) -> None:
        self.query("#option-container > .-active").remove_class("-active")
        if new_selection >= 0:
            self.query_one("#option-container").children[new_selection].add_class(
                "-active"
            )

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if self.selected and action in ("selection_up", "selection_down"):
            return False
        return True

    def action_selection_up(self) -> None:
        self.selection = max(0, self.selection - 1)

    def action_selection_down(self) -> None:
        self.selection = min(len(self.options) - 1, self.selection + 1)

    def action_select(self) -> None:
        self.post_message(self.Response(self.selected))
        self.selected = True


if __name__ == "__main__":
    from textual.app import App
    from textual.widgets import Footer

    OPTIONS = [
        ("Yes, allow once", "proceed_always"),
        ("Yes, allow always", "allow_always"),
        ("Modify with external editor", "modify"),
        ("No, suggest changes (esc)", "reject"),
    ]

    class QuestionApp(App):
        def compose(self) -> ComposeResult:
            yield Question("Apply this change?", OPTIONS)
            yield Footer()

    QuestionApp().run()
