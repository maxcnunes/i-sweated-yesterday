import os

SCHEDULE_AUTH_USERNAME = os.environ['SCHEDULE_AUTH_USERNAME']
SCHEDULE_AUTH_PASSWORD = os.environ['SCHEDULE_AUTH_PASSWORD']

# User role
ADMIN = 0
STAFF = 1
USER = 2
ROLE = {
	ADMIN: 'admin',
	STAFF: 'staff',
	USER: 'user',
}

# User status
INACTIVE = 0
NEW = 1
ACTIVE = 2
STATUS = {
	INACTIVE: 'inactive',
	NEW: 'new',
	ACTIVE: 'active',
}

# Session Name
SESSION_NAME_USER_ID = 'user_id'