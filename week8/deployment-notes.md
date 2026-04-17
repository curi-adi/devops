# Week 8 Deployment - Issues & Fixes

## 1. Terraform version mismatch
`versions.tf` had `required_version = "1.12.1"` (exact pin) but local terraform was 1.14.7.  
**Fix:** changed to `>= 1.12.1`

## 2. S3 state bucket missing
Bucket `state-bucket-768093818017` was deleted after week 6 teardown.  
**Fix:** recreated manually before running `terraform init`
```
aws s3api create-bucket --bucket state-bucket-768093818017 --region ap-south-1 \
  --create-bucket-configuration LocationConstraint=ap-south-1
```

## 3. ECR repos already existed when terraform apply ran
Created the ECR repos manually to push images first, then terraform tried to create them again and threw `RepositoryAlreadyExistsException`.  
**Fix:** imported both repos into state
```
terraform import 'aws_ecr_repository.my_repo["backend"]' devopsdozo-backend
terraform import 'aws_ecr_repository.my_repo["frontend"]' devopsdozo-frontend
```

## 4. Docker context wrong
`docker build` failed with `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`.  
**Fix:** switched context to default
```
docker context use default
```

## 5. Frontend couldn't reach backend (ENOTFOUND backend)
Site loaded but every API call returned 500. Frontend logs showed `ENOTFOUND backend`.  
Root cause: frontend ECS task started ~25 seconds before the backend registered itself in the Service Connect namespace. ECS injects service hostnames at task start, so frontend missed the `backend` entry.  
**Fix:** forced a new frontend deployment after both services were stable
```
aws ecs update-service --cluster aditya-bootcamp-devopsdozo-cluster \
  --service aditya-bootcamp-devopsdozo-frontend-service --force-new-deployment
```
