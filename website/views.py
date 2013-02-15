############################################################################
# This file is part of the Maui Web site.
#
# Copyright (c) 2012 Pier Luigi Fiorini
#
# Author(s):
#    Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# $BEGIN_LICENSE:AGPL3+$
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# $END_LICENSE$
############################################################################

from django.views.generic import View, TemplateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

class ProtectedView(View):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ProtectedView, self).dispatch(*args, **kwargs)

class ProtectedTemplateView(TemplateView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ProtectedTemplateView, self).dispatch(*args, **kwargs)

class ProtectedFormView(FormView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ProtectedFormView, self).dispatch(*args, **kwargs)

class HomeView(TemplateView):
	template_name = "pages/home.html"

class PreviewView(TemplateView):
	template_name = "pages/preview.html"

class DiscoverView(TemplateView):
	template_name = "pages/discover.html"

class ProfileView(ProtectedTemplateView):
	template_name = "registration/profile.html"

class EditProfileView(ProtectedView):
	http_method_names = ["post"]

	def post(self, request, *args, **kwargs):
		# Make sure the user is authenticated
		if not request.user.is_authenticated():
			from django.http import HttpResponseForbidden
			return HttpResponseForbidden()

		from django.utils import simplejson as json
		from django.http import HttpResponse

		pk = int(request.POST["pk"])
		name = request.POST["name"]
		value = request.POST["value"]
		status = 200
		response = None

		try:
			if name == "first_name":
				request.user.first_name = value
			elif name == "last_name":
				request.user.last_name = value
			elif name == "date_of_birth":
				request.user.get_profile().date_of_birth = value
			elif name == "gender":
				request.user.get_profile().gender = value
			elif name == "receive_updates":
				request.user.get_profile().receive_updates = True if value == "true" else False
			else:
				raise Exception("%s is an unknown field" % name)
		except Exception, e:
			response = e.message
			status = 500
		else:
			request.user.save()
			request.user.get_profile().save()

		return HttpResponse(response, status=status, mimetype="text/plain")
