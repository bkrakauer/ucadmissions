from django import forms
import pandas as pd

class ReqForm(forms.Form):
	students = pd.read_csv('students.csv')
	schools = list(students.School.unique())
	list_of_choices = [(school, school) for school in schools]
	gpa = forms.CharField(label="gpa", max_length=6)
	highschool = forms.ChoiceField(choices = list_of_choices)
	# See also with list comprehension -- eg, choices=[(x,x) for x in range(1, 32)]