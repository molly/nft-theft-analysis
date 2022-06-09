from constants import HTML_TOP


def create_report(report_data):
    with open("report.html", "w+", encoding="utf-8") as out:
        out.write(HTML_TOP)
