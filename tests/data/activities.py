"""Test data for activities endpoint"""

ACTIVITIES_POST_DATA = [
    {
        "title": "Jump",
        "dueDate": "2024-12-31T23:59:59Z",
        "completed": True
    },
    {
        "title": "Run",
        "dueDate": "2024-12-25T10:00:00Z",
        "completed": False
    },
    {
        "title": "Walk",
        "dueDate": "2024-12-20T15:30:00Z",
        "completed": True
    }
]

ACTIVITIES_BY_ID_DATA = [
    {
        "id": 1,
        "title": "Activity 1",
        "dueDate": "2024-12-31T23:59:59Z",
        "completed": True
    },
    {
        "id": 2,
        "title": "Activity 2",
        "dueDate": "2024-12-25T10:00:00Z",
        "completed": False
    },
    {
        "id": 3,
        "title": "Activity 3",
        "dueDate": "2024-12-20T15:30:00Z",
        "completed": True
    }
]

ACTIVITIES_UPDATE_DATA = [
    {
        "id": 1,
        "title": "Updated Activity 1",
        "dueDate": "2024-12-31T23:59:59Z",
        "completed": False
    },
    {
        "id": 2,
        "title": "Updated Activity 2",
        "dueDate": "2024-12-25T10:00:00Z",
        "completed": True
    }
]
