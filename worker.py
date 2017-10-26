def update_level():
	for student in Student.objects.all():
		if has_completed_level(student):
			student.level += 100
			student.save()
		else:
			pass