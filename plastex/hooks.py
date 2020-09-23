# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "plastex"
app_title = "Plastex"
app_publisher = "Frappé"
app_description = " App for managing Articles, Members, Memberships and Transactions for Libraries"
app_icon = "octicon octicon-book"
app_color = "grey"
app_email = "info@frappe.io"
app_license = "MIT"
doctype_js = {
	"Purchase Order":"fixtures/custom_scripts/Purchase Order.js"
}
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/plastex/css/plastex.css"
# app_include_js = "/assets/plastex/js/plastex.js"

# include js, css files in header of web template
# web_include_css = "/assets/plastex/css/plastex.css"
# web_include_js = "/assets/plastex/js/plastex.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "plastex.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "plastex.install.before_install"
# after_install = "plastex.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "plastex.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

#doc_events = {
#	"Email Queue": {
# 		"on_change": "plastex.api.reload",
 #		"after_insert": "plastex.api.send_now",
# 		"on_trash": "method"
#	}
#}

# Scheduled Tasks
# ---------------

scheduler_events = {
#	"all": [
#		"plastex.api.send"
#	],
 	"cron": {

		"* * * * *": [
	            "plastex.api.send"
		     
		    
		]
	}
}

# Testing
# -------

# before_tests = "plastex.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "plastex.event.get_events"
# }

