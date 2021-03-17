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
        export BUCKET_NAME=<Bucket name>
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
7. Create an environment variable with the n
ames of the AWS services you want to observe. A full list can be found in .
    ```
        export AWS_SERVICES="aws.<service_1>","aws.<service_2>","aws.<service_3>"
        echo "export AWS_SERVICES=${AWS_SERVICES}" >> ~/.bash_profile
    ```
8. Run the AWS Cloudformation template
    ```
        export AWS_SERVICES="aws.<service_1>","aws.<service_2>","aws.<service_3>"
        echo "export AWS_SERVICES=${AWS_SERVICES}" >> ~/.bash_profile
    ```
9. Create an AWS Cognito user with a temporal password to access Kibana. 
    ```
        export AWS_SERVICES="aws.<service_1>","aws.<service_2>","aws.<service_3>"
        echo "export AWS_SERVICES=${AWS_SERVICES}" >> ~/.bash_profile
    ```