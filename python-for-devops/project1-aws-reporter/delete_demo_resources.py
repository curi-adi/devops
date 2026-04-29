import boto3

REGION = "ap-south-1"

ec2 = boto3.client("ec2", region_name=REGION)
sm = boto3.client("secretsmanager", region_name=REGION)

SECRET_NAMES = ["adi-demo/db-password", "adi-demo/api-key"]


def terminate_instances():
    try:
        with open("demo_instance_ids.txt") as f:
            ids = [line.strip() for line in f if line.strip()]
        ec2.terminate_instances(InstanceIds=ids)
        print(f"Terminated instances: {ids}")
    except FileNotFoundError:
        print("demo_instance_ids.txt not found — nothing to terminate")


def delete_secrets():
    for name in SECRET_NAMES:
        try:
            sm.delete_secret(SecretId=name, ForceDeleteWithoutRecovery=True)
            print(f"Deleted secret: {name}")
        except sm.exceptions.ResourceNotFoundException:
            print(f"Secret not found (already deleted?): {name}")


print("Terminating EC2 instances...")
terminate_instances()

print("\nDeleting Secrets Manager secrets...")
delete_secrets()

print("\nAll demo resources deleted.")
