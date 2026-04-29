import boto3


def get_ec2_client(region):
    return boto3.client("ec2", region_name=region)


def get_secretsmanager_client(region):
    return boto3.client("secretsmanager", region_name=region)


def list_ec2_instances(region):
    client = get_ec2_client(region)
    response = client.describe_instances()
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            name = ""
            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]
            instances.append([
                instance.get("InstanceId", ""),
                instance.get("State", {}).get("Name", ""),
                instance.get("InstanceType", ""),
                name,
                region,
            ])
    return instances


def list_secrets(region):
    client = get_secretsmanager_client(region)
    response = client.list_secrets()
    secrets = []
    for secret in response.get("SecretList", []):
        secrets.append([
            secret.get("Name", ""),
            secret.get("ARN", ""),
            str(secret.get("CreatedDate", "")),
            str(secret.get("LastChangedDate", "")),
            region,
        ])
    return secrets


def accumulate_ec2_data(regions):
    all_data = []
    for region in regions:
        all_data.extend(list_ec2_instances(region))
    return all_data


def accumulate_secrets_data(regions):
    all_data = []
    for region in regions:
        all_data.extend(list_secrets(region))
    return all_data
