from apscheduler.scheduler import Scheduler

from app.users.notifications import send_email_to_users_have_forgotten_add_last_exercise


sched = Scheduler()

# Execute everyday at 13:30 UTC SP-BR
@sched.cron_schedule(hour=13, minute=30)
def scheduled_job():
	# send notification
	send_email_to_users_have_forgotten_add_last_exercise()

sched.start()

while True:
	pass