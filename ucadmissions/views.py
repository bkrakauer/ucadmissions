from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from sklearn import neighbors
from sklearn.externals import joblib
from .forms import ReqForm
import numpy as np
import matplotlib.pyplot as plt
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.charts import Scatter
from bokeh.models import Axis

def index(request):
	students = pd.read_csv('students.csv')
	context = {'schools': list(students.School.unique())}
	#return HttpResponse("At Index!")
	return render(request, 'index.html', context)
	
def results(request):
	knnmodel = joblib.load('knnmodel.pkl')
	students = pd.read_csv('students.csv')
	if request.method == "POST":
		form = ReqForm(request.POST)
		if form.is_valid():
			gpa = form.cleaned_data['gpa']
			school = form.cleaned_data['highschool']
			income = students[students.School == school].iloc[0,3]
			data = np.array([gpa, income]).reshape(1,-1)
			prediction = knnmodel.predict_proba(data)
			prediction = round(prediction[0][1], 2) * 100
			(script, div) = get_plot(students, gpa, income)
			context = {'highschool': school, 'gpa': gpa, 'prediction': prediction, 'script': script, 'div': div}
			return render(request, 'results.html', context)
		else:
			print "Form invalid for some reason."
			return render(request, 'index.html')

def get_plot(students, gpa, income):
	print "In get_plot"
	s = students.sample(frac=.08)
	s.Admitted = s.Admitted.apply(lambda x: "Admitted" if x == 1 else "Not Admitted")
	s = s.append({'Admitted': "You", 'Income': int(income), 'Student GPA': float(gpa)}, ignore_index=True)
	plot = Scatter(s, x="Student GPA", y="Income", color="Admitted", title="Income and GPA", ylabel="Zip Code Income", webgl=True)
	yaxis = plot.select(dict(type=Axis, layout="left"))[0]
	yaxis.formatter.use_scientific = False
	script, div = components(plot)
	return (script, div)
	