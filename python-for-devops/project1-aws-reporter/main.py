import argparse
from aws_data import accumulate_ec2_data, accumulate_secrets_data
from excel_writer import write_to_excel


def main():
    parser = argparse.ArgumentParser(description="AWS Resource Reporter - exports EC2 and Secrets to Excel")
    parser.add_argument("--regions", nargs="+", default=["ap-south-1"], help="AWS regions to query")
    args = parser.parse_args()

    regions = args.regions
    print(f"Fetching data for regions: {regions}")

    ec2_headers = ["Instance ID", "State", "Instance Type", "Name", "Region"]
    ec2_data = accumulate_ec2_data(regions)
    print(f"Found {len(ec2_data)} EC2 instances")

    secrets_headers = ["Name", "ARN", "Created Date", "Last Changed", "Region"]
    secrets_data = accumulate_secrets_data(regions)
    print(f"Found {len(secrets_data)} secrets")

    write_to_excel(
        filename="aws_report.xlsx",
        sheets={
            "EC2 Instances": (ec2_headers, ec2_data),
            "Secrets Manager": (secrets_headers, secrets_data),
        }
    )
    print("Report saved to aws_report.xlsx")


if __name__ == "__main__":
    main()
