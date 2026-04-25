import json
from datetime import datetime


def get_current_time():
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


def list_mock_emails():
    emails = [
        {
            "from": "sarah@company.com",
            "subject": "Q3 deployment update",
            "snippet": "Hey, just confirming the rollout is on track for Friday...",
            "received": "2026-04-24T09:15:00",
            "unread": True,
        },
        {
            "from": "noreply@github.com",
            "subject": "[jarvis] PR #2 merged",
            "snippet": "Your pull request was merged into main...",
            "received": "2026-04-24T08:02:00",
            "unread": False,
        },
        {
            "from": "raj@team.io",
            "subject": "Lunch tomorrow?",
            "snippet": "Free around 1pm? Want to grab tacos at that new place...",
            "received": "2026-04-23T16:48:00",
            "unread": True,
        },
    ]
    return json.dumps(emails, indent=2)


def list_mock_calendar():
    events = [
        {
            "title": "Standup",
            "start": "2026-04-25T09:30:00",
            "end": "2026-04-25T09:45:00",
            "attendees": ["team@company.com"],
        },
        {
            "title": "1:1 with manager",
            "start": "2026-04-25T14:00:00",
            "end": "2026-04-25T14:30:00",
            "attendees": ["manager@company.com"],
        },
        {
            "title": "Deploy review",
            "start": "2026-04-25T16:00:00",
            "end": "2026-04-25T17:00:00",
            "attendees": ["sarah@company.com", "raj@team.io"],
        },
    ]
    return json.dumps(events, indent=2)


tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_current_time',
            'description': 'Get the current date and time',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'list_mock_emails',
            'description': 'List the user\'s recent emails. Returns sender, subject, snippet, received timestamp, and read status as JSON.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'list_mock_calendar',
            'description': 'List the user\'s upcoming calendar events. Returns title, start time, end time, and attendees as JSON.',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            },
        },
    },
]


def handle_tool_call(tool_call):
    fn_name = tool_call.function.name if hasattr(tool_call, 'function') else tool_call['function']['name']

    dispatch = {
        'get_current_time': get_current_time,
        'list_mock_emails': list_mock_emails,
        'list_mock_calendar': list_mock_calendar,
    }

    fn = dispatch.get(fn_name)
    if fn is None:
        return f"Unknown tool: {fn_name}"

    return fn()