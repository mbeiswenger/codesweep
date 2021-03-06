from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainapp.models import Assignment, Submission, Course
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.http import require_http_methods
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.conf import settings
from django.shortcuts import redirect

# modules for code submission
import os
import datetime
import re

import sys

def index(request):
	if request.user.is_authenticated():
		return redirect('/assignments/')
	else:
		# an inactive account was used
		return render(request, 'mainapp/login.html')


@login_required
def assignments(request):

	terms = Course.objects.filter(students = request.user).values('term__season', 'term__year').distinct()
	courses = Course.objects.filter(students = request.user)
	assignments = Assignment.objects.filter(course__in=courses)

	# if request.method == 'POST':
	#
	# 	# retrive ajax data
	# 	data = request.POST
	# 	course_subject = data['course_subject']
	# 	course_number = data['course_number']
	# 	course_section = data['course_section']
	# 	term_season = data['term_season']
	# 	term_year = data['term_year']
	#
	# 	# get the associated course for the click
	# 	course = Course.objects.filter(subject = course_subject,
	# 								number = course_number,
	# 								section = course_section,
	# 								term__year = term_year,
	# 								term__season = term_season)
	#
	# 	# get the assignments associated with that course
	# 	assignments = Assignment.objects.filter(course = course)

	context_dict = {
		'assignments': assignments,
		'courses': courses,
		'terms': terms,
	}

	return render(request, 'mainapp/assignments.html', context_dict)

@login_required
def show_assignment(request, assignment_name_slug):
	try:
		context_dict = {}
		assignment = Assignment.objects.get(slug=assignment_name_slug)
		context_dict['assignment'] = assignment
	except Assignment.DoesNotExist:
		context_dict['assignment'] = None

	return render(request, 'mainapp/projectpage.html', context_dict)

def find_assignments(request):

	if request.method == 'POST':

		# retrive ajax data
		data = request.POST
		course_subject = data['course_subject']
		course_number = data['course_number']
		course_section = data['course_section']
		term_season = data['term_season']
		term_year = data['term_year']

		# terms in which user is enrolled
		terms = Course.objects.filter(students = request.user).values('term__season', 'term__year').distinct()

		# courses in which user is enrolled
		courses = Course.objects.filter(students = request.user)

		# get the associated course for the click
		course = Course.objects.get(subject = course_subject,
									number = course_number,
									section = course_section,
									term__year = term_year,
									term__season = term_season)

		# get the assignments associated with that course
		assignments = Assignment.objects.filter(course = course)

		assignments_html = []
		assignments_html += '<div class="display-4 mt-5 text-center">' + str(course.subject + ' ' + course.number + ' ' + course.section) + '</div>'
		for assignment in assignments:
			assignments_html += '<div class="card mt-5"><div class="card-header"><div>' + \
				'Due ' + str(assignment.date_due.strftime('%B %d, %Y')) + ' at ' +  str(assignment.time_due.strftime('%-I %p')) + \
				'<div class="float-right">' + \
				'Points: ' + str(assignment.points) + \
				'</div></div></div>' + \
				'<div class="card-body">' + \
				'<h5 class="card-title">' + assignment.title + '</h5>' + \
				'<p class="card-text">' + assignment.description + '</p>' + \
				'<a href="' + assignment.slug + '" class="btn btn-primary float-right btn-info">Get Started</a>' + \
				'</div></div>'

		assignments_html = "".join(assignments_html);

		# create JSON data response
		data = {
			'assignments_html': assignments_html,
		}

		return JsonResponse(data)

	else:
			raise Http404()


def submit_text(request):

	if request.method == 'POST':



		data = request.POST # retrieve data

		code = data['code_text'] # obtain submitted code
		user = data['user'] # obtain the user submitting the code
		assignment_title = data['assignment_title'] # obtain assignment title

		code = code[1:-1] # remove beginning and end quotes

		# retrieve data about this homework assignment from the db
		function_definition = Assignment.objects.get(title=assignment_title).function_definition
		inputs = Assignment.objects.get(title=assignment_title).inputs
		expected_outputs = Assignment.objects.get(title=assignment_title).outputs
		function_name = re.sub(r'\([^)]*\)', '', function_definition)

		# retrieve assignment object to be used in submission record
		current_assignment = Assignment.objects.get(title=assignment_title)

		# replace spaces with underscores
		# so the title can be used in a filename
		assignment_title = assignment_title.replace(" ", "+")




		# date and time of submission, to be used in filename
		currentDT = datetime.datetime.now()
		currentDT = currentDT.strftime("%Y-%m-%d--%H-%M-%S")

		# create unique filenames for code file and output file
		python_code_file = "{}--{}--{}.py".format(
								user, assignment_title, currentDT)
		code_output_file = "{}--{}--{}--outputs.txt".format(
								user, assignment_title, currentDT)


		# un-escape backslash-escaped code string
		code = bytes(code, "utf-8").decode("unicode_escape")

		# create paths for submission files
		code_path = os.path.join(settings.MEDIA_ROOT, 'code')
		inputs_path = os.path.join(settings.MEDIA_ROOT, 'inputs', assignment_title)
		expected_outputs_path = os.path.join(settings.MEDIA_ROOT, 'expectedoutputs', assignment_title)
		code_output_path = os.path.join('temp_files', 'code_output_files')
		diff_path = os.path.join('temp_files', 'diff_files')
		error_path = os.path.join('temp_files', 'error_files')

		# create directories if they do not already exist
		if not os.path.exists(code_path):
			os.makedirs(code_path)
		if not os.path.exists(inputs_path):
			os.makedirs(inputs_path)
		if not os.path.exists(expected_outputs_path):
			os.makedirs(expected_outputs_path)
		if not os.path.exists(code_output_path):
			os.makedirs(code_output_path)
		if not os.path.exists(diff_path):
			os.makedirs(diff_path)
		if not os.path.exists(error_path):
			os.makedirs(error_path)

		# append files to each path
		code_path = os.path.join(code_path, python_code_file)
		inputs_path = os.path.join(inputs_path, 'inputs.txt')
		expected_outputs_path = os.path.join(expected_outputs_path, 'expected--outputs.txt')
		code_output_path = os.path.join(code_output_path, code_output_file)

		# create inputs file
		with open(inputs_path, 'w') as inputs_file:
			for item in inputs:
					inputs_file.write(item)

		# add newline at end of expected outputs as best practice
		# https://stackoverflow.com/questions/5813311/no-newline-at-end-of-file
		expected_outputs += "\n"
		# create expected outputs file
		with open(expected_outputs_path, 'w') as expected_outputs_file:
			for item in expected_outputs:
				expected_outputs_file.write(item)

# ------- PARSING INPUTS ----------------- #




		with open(inputs_path, 'r') as input_file, open(code_path, 'w') as code_file:

			code_file.write(code)
			code_file.write("\n\n")
			code_file.write("import sys")
			code_file.write("\n\n")
			code_file.write("def Main():\n\t")
			code_file.write("with open(sys.argv[1], 'r') as input, open(sys.argv[2], 'w') as output:\n\t\t")

			# assume that we are not in double quotes
			inDoubleQuotes = False

			variable = ""
			numVariable = ""
			variableList = []


			for line in input_file:
				for index, c in enumerate(line):

					if inDoubleQuotes:
						if line[index] == "\\" and line[index + 1] == "\"":
							continue
						else:
							variable += c

					# negative integers
					if not inDoubleQuotes and index > 0 and c.isdigit() and line[index - 1] == "-":
						neg_num = "-" + c
						numVariable += neg_num

					# positive integers
					elif not inDoubleQuotes and c.isdigit():
						numVariable += c


					if not inDoubleQuotes and line[index:index + 5] == "False":
						variableList.append("False")

					if not inDoubleQuotes and line[index:index + 4] == "True":
						variableList.append("True")

					# account for the beginning of iteration
					if index == 0 and line[index] == "\"":
						inDoubleQuotes = not inDoubleQuotes


					# if we come across an unescaped quote, toggle inDoubleQuotes
					if index != 0 and line[index - 1] != "\\" and line[index] == "\"":
						inDoubleQuotes = not inDoubleQuotes


				# ------- four instances in which we write to file -------- #

				# (1) if we are not in double quotes and we come across a ","
				#     append the variable and make it empty for the next variable
					if not inDoubleQuotes and line[index] == ",":
						if variable:
							variableList.append("str('" + variable[:-1] + "')")
							variable = ""
						if numVariable:
							variableList.append("int(" + numVariable + ")")
							numVariable = ""

				# (2) if we are at the last index and we are accounting for an integer
					if not inDoubleQuotes and index == len(line) - 1:
						if numVariable:
							variableList.append("int(" + numVariable + ")")
							numVariable = ""

				# (3) if we are at the last index of a string with closing double quote
					if not inDoubleQuotes and line[index] == "\"" and index == len(line) - 1:
						if variable:
							variableList.append("str('" + variable[:-1] + "')")
							variable = ""


				# (4) if we are at the last index of a string with closing double quote and newline
					if not inDoubleQuotes and index == len(line) - 1 and line[index] == "\n" and line[index - 1] == "\"":
						if variable:
							variableList.append("str('" + variable[:-1] + "')")
							variable = ""

				variableList = ', '.join(variableList)
				code_file.write("output.write(str(" + function_name + "(" + variableList + ")) + '\\n')\n\t\t")
				variableList = []


			code_file.write("\n\n")
			code_file.write("if __name__ == '__main__':\n\t")
			code_file.write("Main()")





# ------- PARSING INPUTS ----------------- #

		# take in file input
		# create outputs file and error file
		os.system('python3 {} {} {} 2> temp_files/error_files/error.txt'.format(code_path, inputs_path, code_output_path))

		os.system('diff --strip-trailing-cr {} {} | cat -t > temp_files/diff_files/diff-results.txt'.format(code_output_path, expected_outputs_path))

		# read the error file
		with open('temp_files/error_files/error.txt', 'r') as error_file:
			# skip the lines relating to traceback to Main()
			errorfile = error_file.readlines()[5:]
		errorfile = "".join(errorfile)

		# read the outputs file
		with open(code_output_path, 'r') as output_file:
			outputfile = output_file.read()

		try:
			with open(code_output_path, 'rb+') as f:
				f.seek(-1, os.SEEK_END)
				f.truncate()
		except OSError:
			print("Cannot remove lines from empty file")


		# read the outputs file
		with open('temp_files/diff_files/diff-results.txt', 'r') as diff_file:
			diff_results = diff_file.read()


		# --------- calculate code/comment ratio ------------- #

		# sum of comments
		# capture any characters between # and \n
		comments = re.findall(r"#.*\n|#.*", code)
		comments = str(comments)
		# remove erroneous characters
		comments = comments.replace("[", "")
		comments = comments.replace("]", "")
		comments = comments.replace("\\n", "")
		comments = comments.replace(" ", "")
		comments = comments.replace(",", "")
		comments = comments.replace("'", "")
		# sum characters in comment string
		comment_sum = 0
		for item in comments:
			comment_sum += 1

		# sum of code
		code = code.replace("\n", "")
		code = code.replace("\t", "")
		code_sum = 0
		for item in code:
			code_sum += 1

		comment_code_ratio = (comment_sum/code_sum)*100


		# ----------------------------------------------------- #

		correct = True
		if (diff_results):
			correct = False

		# -- obtain foreign fields from the db
		# obtain the db object for the current user
		current_user = User.objects.get(username=user)

		# change the code path so that the server
		# can find it's address relative to the site's main page
		# if this wasn't changed, it would include the entire path
		# on the computer. For example, users/documents/python/codesweep/ etc...
		code_path = os.path.join('code', python_code_file)


		# create submission record
		submission = Submission()
		submission.user = current_user
		submission.assignment = current_assignment
		submission.file = code_path
		submission.date_submitted = datetime.datetime.now()
		submission.time_submitted = datetime.datetime.now()
		submission.correct = correct
		submission.comment_ratio = comment_code_ratio
		submission.save()


		# create JSON data response
		data = {
			'error': errorfile,
			'output': outputfile,
			'comment_ratio': comment_code_ratio,
			'diff_results': diff_results
		}

		return JsonResponse(data)

	else:
		raise Http404()



@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))



def user_login(request):

	if request.method == 'POST':

		# retrieve username and password
		username = request.POST.get('username')
		password = request.POST.get('password')

		# authenticate user
		user = authenticate(username=username, password=password)

		# if we have a User object, the details are correct
		# if None (Python's way of representing the absence of a value), no user
		# with matching credentials was found
		if user:

			# check that account is not disabled
			if user.is_active:

				# log the user in
				login(request, user)
				return redirect('/assignments/')
			else:

				# an inactive account was used
				return HttpResponse("Your account is disabled.")
		else:

			# no user credentials were found
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")

	# the request is not a HTTP POST
	else:
		raise Http404()
