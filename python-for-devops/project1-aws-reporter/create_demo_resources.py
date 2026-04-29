import boto3
import time

REGION = "ap-south-1"
AMI_ID = "ami-09d623d7034669ca5"
INSTANCE_TYPE = "t3.micro"

ec2 = boto3.client("ec2", region_name=REGION)
sm = boto3.client("secretsmanager", region_name=REGION)


def create_instances():
    instances_config = [
        {"Name": "adi-demo-webserver", "tag": "web"},
        {"Name": "adi-demo-appserver", "tag": "app"},
        {"Name": "adi-demo-dbproxy", "tag": "db"},
    ]
    instance_ids = []
    for cfg in instances_config:
        resp = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            MinCount=1,
            MaxCount=1,
            SubnetId="subnet-0a5cbcd47fab56c80",
            TagSpecifications=[{
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": cfg["Name"]},
                    {"Key": "Project", "Value": "adi-bootcamp-demo"},
                ]
            }]
        )
        iid = resp["Instances"][0]["InstanceId"]
        instance_ids.append(iid)
        print(f"  Launched: {iid}  ({cfg['Name']})")
    return instance_ids


def create_secrets():
    secrets_config = [
        {"name": "adi-demo/db-password", "value": '{"username":"admin","password":"DemoPass123"}'},
        {"name": "adi-demo/api-key", "value": '{"api_key":"demo-key-abc123"}'},
    ]
    for cfg in secrets_config:
        try:
            resp = sm.create_secret(Name=cfg["name"], SecretString=cfg["value"])
            print(f"  Created secret: {resp['Name']}")
        except sm.exceptions.ResourceExistsException:
            print(f"  Secret already exists: {cfg['name']}")


print("Creating 3 EC2 instances...")
ids = create_instances()

print("\nCreating 2 Secrets Manager secrets...")
create_secrets()

print("\nWaiting 15s for instances to initialise...")
time.sleep(15)
print("Done. Run main.py to generate the report.")

with open("demo_instance_ids.txt", "w") as f:
    f.write("\n".join(ids))
print(f"Instance IDs saved to demo_instance_ids.txt")
