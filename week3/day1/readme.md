# user data script to be copied on launch template

```bash
#!/bin/bash

sleep 30
sudo yum update -y

echo "Installing git" >> /home/ec2-user/install.log
sudo yum install git -y 


cd /home/ec2-user
echo "$(pwd) " >> /home/ec2-user/install.log


echo "cloning code " >> /home/ec2-user/install.log
git clone https://github.com/devopswithakhilesh/Jan26-devops-bootcamp

cd Jan26-devops-bootcamp/week3/day1/app

echo "in app $(pwd) " >> /home/ec2-user/install.log

chmod u+x run.sh

echo "Starting the app " >> /home/ec2-user/install.log

./run.sh 

```