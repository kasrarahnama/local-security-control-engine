import boto3

class CloudTrailEvidenceCollector:

    def __init__(self):
        self.client = boto3.client("cloudtrail")

    def get_trails(self):
        response = self.client.describe_trails()
        return response.get("trailList", [])

    def check_logging(self):
        trails = self.get_trails()
        results = []

        for trail in trails:
            status = self.client.get_trail_status(Name=trail["Name"])
            results.append({
                "trail_name": trail["Name"],
                "is_logging": status["IsLogging"]
            })

        return results