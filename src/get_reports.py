import requests
import json

def get_congress_reports(num_congress=118, chamber="hrpt"):
    """
    chamber: hrpt, srpt
    """
    res = requests.get(
        f"https://www.govinfo.gov/wssearch/rb/crpt/{num_congress}/{chamber}?fetchChildrenOnly=1&pageSize=0&offset=0&sortDirection=1"
    )
    data = res.json()

    reports = data["childNodes"]

    for report in reports:
        try:
            yield dict(
                chamber=chamber,
                report_id = report["nodeValue"]["granuleid"],
                report_pdf_url = f"https://www.govinfo.gov/content/pkg/{report['nodeValue']['pdffile']}",
                report_title = report["nodeValue"]["title"],
                report_committee = report["nodeValue"]["committee"],
                report_publish_date = report["nodeValue"]["publishdate"],
            )
        except:
            import pdb
            pdb.set_trace()

def get_all_reports(num_congress=118):
    chambers = ["hrpt","srpt"]
    results = []
    for chamber in chambers:
        reports = get_congress_reports(num_congress, chamber)
        for report in reports:
            results.append(report)
    with open("frontend/data.json", "w") as fp:
        json.dump(results, fp, indent=2)
    return True

if __name__ == "__main__":
    get_all_reports()
