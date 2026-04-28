from memory import clear_history
from tools import list_tool_names


COMMANDS_HELP = """
Commands:
  /help      - show this help
  /clear     - wipe conversation memory
  /history   - show recent messages
  /tools     - list available tools
  quit/exit  - leave Jarvis
"""


def handle_command(cmd, messages):
    """Returns (handled, new_messages). handled=True means input was a command."""
    if cmd == '/help':
        print(COMMANDS_HELP)
        return True, messages

    if cmd == '/clear':
        clear_history()
        print("Memory wiped.\n")
        return True, []

    if cmd == '/history':
        if not messages:
            print("No history.\n")
            return True, messages
        print("\n--- recent ---")
        for m in messages[-10:]:
            role = m.get('role', '?')
            content = (m.get('content') or '')[:80]
            print(f"  [{role}] {content}")
        print("--- end ---\n")
        return True, messages

    if cmd == '/tools':
        print("Available tools:")
        for name in list_tool_names():
            print(f"  - {name}")
        print()
        return True, messages

    return False, messages