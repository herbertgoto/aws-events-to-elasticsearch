# aws-events-to-elasticsearch
Sends EventBridge AWS events to elasticsearch

## How to install

You can run these steps from your own terminal. However, for the sake of simplicity this instructions will use AWS CloudShell. 

1. From the AWS Console, make your you are in the region where you want to deploy the solution and access AWS CloudShell service.   
2. Revisit the policies attached to your principal(user/role) and make sure it has the AdministratorAccess policy attached. Run the following command to get the principal:
    ```
        aws sts get-caller-identity
    ```
3. Create an S3 Bucket
    ```
        aws s3 mb s3://<Bucket name> --region $AWS_REGION
    ```
4. Create an environment variable for your bucket name. 
    ```
        export BUCKET_NAME=<Enter your bucket name>
        echo "export BUCKET_NAME=${BUCKET_NAME}" >> ~/.bash_profile
    ```
5. Clone this repo
    ```
        git clone https://github.com/herbertgoto/aws-events-to-elasticsearch.git
    ```
6. Execute the setup code to update the workspace libraries and package and upload code to S3.
    ```
        chmod 700 aws-events-to-elasticsearch/setup/setup.sh 
        aws-events-to-elasticsearch/setup/setup.sh
    ```
7. Create an environment variable with the code bindings for the AWS services you want to observe - __[Tutorial: Download Code Bindings for Events using the EventBridge Schema Registry](https://docs.aws.amazon.com/eventbridge/latest/userguide/eventbridge-tutorial-schema-download-binding.html)__
    ```
        export AWS_SERVICES='"aws.<Enter AWS service 1 code binding>"','"aws.<Enter AWS service 1 code binding>"'
        echo "export AWS_SERVICES=${AWS_SERVICES}" >> ~/.bash_profile
    ```
8. Run the AWS Cloudformation template. For this you have to define an unique __[User Pool Domain](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-assign-domain.html)__
    ```
        aws cloudformation deploy --template-file aws-events-to-elasticsearch/setup/solution-cfn.yaml \
        --stack-name <Enter stack name> --capabilities CAPABILITY_IAM \
        --parameter-overrides UserPoolDomain=<Enter name for the user pool domain> \
        LambdaCodeBucket=$BUCKET_NAME AWSServices=$AWS_SERVICES
    ```
9. Create an AWS Cognito user with a temporal password to access Kibana. 
    ```
        aws cognito-idp admin-create-user --username <Enter email address> \
        --temporary-password <Enter temporary password> \
        --user-pool-id $(aws cloudformation describe-stacks --stack-name <Enter stack name> | jq -r '[.Stacks[0].Outputs[] | {key: .OutputKey, value: .OutputValue}] | from_entries'.ESCognitoUserPool) 
    ```