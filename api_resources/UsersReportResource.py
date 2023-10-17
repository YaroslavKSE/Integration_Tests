from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sql_db_models.sql_user_statistics_models import *

app = Flask(__name__)
api = Api(app)


class UsersReportResource(Resource):
    reports = {}  # A class variable to store reports for simplicity.

    def get(self, report_name):
        date_from = request.args.get('from')
        date_to = request.args.get('to')

        # To do: Filter the data based on date_from and date_to if necessary.

        report_data = self.reports.get(report_name, {})
        response_data = [{'userId': user, 'metrics': metrics} for user, metrics in report_data.items()]

        return jsonify(response_data)

    def post(self, report_name):
        # Parse the request body
        body = request.get_json()
        metrics = body.get('metrics', [])
        users = body.get('users', [])

        # Generate the report (this is where we'll calculate all the required metrics)
        report_data = self.generate_report(metrics, users)
        self.reports[report_name] = report_data

        return jsonify({})

    @staticmethod
    def generate_report(metrics, users):
        report_data = {}

        for user in users:
            user_metrics = {}
            for metric in metrics:
                if metric == "daily_average":
                    user_metrics["dailyAverage"] = calculate_daily_average(user)
                elif metric == "weekly_average":
                    user_metrics["weeklyAverage"] = calculate_weekly_average(user)
                elif metric == "total":
                    user_metrics["total"] = calculate_total_online_seconds(user)
                elif metric == "min":
                    user_metrics["min"] = calculate_daily_min_seconds(user)
                elif metric == "max":
                    user_metrics["max"] = calculate_daily_max_seconds(user)

            report_data[user] = user_metrics

        # For now, let's just print the report data.
        print(report_data)

        return report_data


if __name__ == '__main__':
    app.run(debug=True)
