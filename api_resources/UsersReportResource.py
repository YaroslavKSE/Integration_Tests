from flask import request, jsonify
from flask_restful import Resource
from sql_db_models.sql_user_statistics_models import *

reports = {}
report_configs = {}


class UsersReportResource(Resource):
    @staticmethod
    def get(report_name):
        date_from = request.args.get('from')
        date_to = request.args.get('to')

        # To do: Filter the data based on date_from and date_to if necessary.

        report_data = reports.get(report_name, {})
        # List to store users and their metrics
        users_list = []

        # Variables to calculate global metrics
        total_daily_average = 0
        total_weekly_average = 0
        num_users = 0
        for user, metrics in report_data.items():
            if isinstance(metrics, str):  # For "Error: user not found" cases
                user_entry = {
                    "userId": user,
                    "metrics": metrics
                }
            else:
                user_entry = {
                    "userId": user,
                    "metrics": [dict([item]) for item in metrics.items()]
                }
                total_daily_average += metrics.get('dailyAverage', 0)
                total_weekly_average += metrics.get('weeklyAverage', 0)
                num_users += 1

            users_list.append(user_entry)

            # Calculate average metrics for all users
        average_daily_average = total_daily_average / num_users if num_users else 0
        average_weekly_average = total_weekly_average / num_users if num_users else 0

        response_data = {
            "Users": users_list,
            "dailyAverage": average_daily_average,
            "weeklyAverage": average_weekly_average,
        }

        return jsonify(response_data)

    def post(self, report_name):
        # Parse the request body
        body = request.get_json(force=True)
        metrics = body.get('metrics', [])
        users = body.get('users', [])

        # Save the configuration
        report_configs[report_name] = {
            "Name": report_name,
            "metrics": metrics,
            "users": users
        }

        # Generate the report (this is where we'll calculate all the required metrics)
        report_data = self.generate_report(metrics, users)
        reports[report_name] = report_data

        return jsonify({})

    @staticmethod
    def generate_report(metrics, users):
        report_data = {}

        for user in users:
            if user_exists_in_db(user):
                user_metrics = {}
                for metric in metrics:
                    if metric == "dailyAverage":
                        user_metrics["dailyAverage"] = calculate_daily_average(user)
                    elif metric == "weeklyAverage":
                        user_metrics["weeklyAverage"] = calculate_weekly_average(user)
                    elif metric == "total":
                        user_metrics["total"] = calculate_total_online_seconds(user)
                    elif metric == "min":
                        user_metrics["min"] = calculate_daily_min_seconds(user)
                    elif metric == "max":
                        user_metrics["max"] = calculate_daily_max_seconds(user)

                report_data[user] = user_metrics
            else:
                report_data[user] = "Error: user not found"

        return report_data
