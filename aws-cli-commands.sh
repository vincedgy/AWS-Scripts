
# List available AWS images
aws ec2 describe-images --owners self amazon --query 'Images[*].{ImageId:ImageId,CreationDate:CreationDate,Public:Public,Description:Description}' --output text --max-items 10 | sort -k 1 

aws ec2 describe-images --owners amazon --filter Name="description",Values="Amazon Linux AMI*" --query 'Images[].[ImageId,CreationDate,Public,Name,Description]' --output text | sort -r -k 2 | head -5

# List EC2 instances
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,LaunchTime]' --output text | sort -n -k 2

# List volumes
aws ec2 describe-volumes --output text

# List EC2 
aws ssm describe-instance-information --instance-information-filter-list key=PingStatus,valueSet=Online

# List Instances profile
aws iam list-instance-profiles

# Remove instance-profile based on a RoleName
export ROLE_NAME=RunCommandRole
for INSTANCE_PROFILE_NAME in $(aws iam list-instance-profiles-for-role --role-name $ROLE_NAME --query "InstanceProfiles[].{InstanceProfileName:InstanceProfileName}" --output text)
do
    aws iam remove-role-from-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME --role-name $ROLE_NAME
    aws iam delete-instance-profile --instance-profile-name $INSTANCE_PROFILE_NAME
done