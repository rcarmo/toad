from typing import TypedDict, Literal

type Tag = Literal["coding", "chat"]
"""A tag used for categorizing the agent. Currently only 'coding' or 'chat'."""
type OS = Literal["macos", "linux", "windows", "*"]
"""An operating system identifier, or a '*" wildcard, if it is the same for all OSes."""
type Action = Literal["install", "uninstall", "update"]
"""An action which the agent supports."""
type AgentType = Literal["coding", "chat"]
"""The type of agent."""


class Script(TypedDict):
    """Used to perform an action associate with an Agent."""

    description: str
    """Describes what the script will do. For example: 'Install Claude Code'."""
    type: str
    """The type of script. For now, this is expected to be 'bash'."""
    script: str
    """The script (such as a bash script)."""


class Agent(TypedDict):
    """Describes an agent which Toad can connect to. Currently only Agent Client Protocol is supported."""

    identity: str
    """A unique identifier for this agent useable as a filename. Typically domain like, although the domain doesn't need to exist. For example: 'claude.anthropic.ai'."""
    name: str
    """The name of the agent. For example: 'Claude Code'."""
    type: AgentType
    """The type of agent. Currently only 'acp' is supported."""
    short_name: str
    """A short name, usable on the command line. For example: 'claude'."""
    author_name: str
    """The author of the agent. For example 'Anthropic'."""
    author_url: str
    """The authors homepage. For example 'https://www.anthropic.com/'."""
    publisher_name: str
    """The publisher's name (an individual or organization that wrote this data)."""
    publisher_url: str
    """The publisher's url."""
    description: str
    """A description of the agent. A few sentences max."""
    tags: list[Tag]
    """Tags which identifies the type of agent. Must not be empty. For agents it will typically be `['coding']`."""

    help: str
    """A Markdown document with additional details regarding the agent."""

    run_command: dict[OS, str]
    """Command to run the agent, by OS or wildcard."""

    scripts: dict[OS, dict[Action, Script]]
    """Scripts to perform actions, typically at least to install the agent."""


class InstalledAgent(TypedDict):
    identity: str
    """Identity of installed agent (matches Agent['identity'])"""
    name: str
    """Long form name of agent."""
    short_name: str
    """Short name of agent (used when launching from the command line)."""
    run_command: dict[OS, str]
