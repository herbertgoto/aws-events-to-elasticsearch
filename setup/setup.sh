#!/bin/bash

if [ -n "$BUCKET_NAME" ]
then
    echo 'Upgrading/Installing libraries and packages'
    # Update instance and install packages
    sudo yum update -y
    sudo yum install -y jq moreutils

    # Upgrade pip
    sudo pip3 install --upgrade pip
    echo "export PATH=~/.local/bin:$PATH" >> ~/.bash_profile
    source ~/.bash_profile

    # Upgrade awscli
    pip3 install awscli --upgrade --user
    source ~/.bash_profile

    echo 'Packaging and uploading lambda code to send dlq messages to S3'
    # Upload Lambda Code
    mkdir app-dql-to-s3
    cp aws-events-to-elasticsearch/dlq-to-s3-function/* app-dql-to-s3/
    cd app-dql-to-s3
    python -m venv dlqLambda
    source dlqLambda/bin/activate
    mv lambda_function.py dlqLambda/lib/python*/site-packages/
    mv requirements.txt dlqLambda/lib/python*/site-packages/
    cd dlqLambda/lib/python*/site-packages/
    pip install -r requirements.txt 
    deactivate
    mv ../dist-packages/* .
    zip -r9 dlqLambdaFunction.zip .
    aws s3 cp dlqLambdaFunction.zip s3://$BUCKET_NAME

    echo 'Packaging and uploading lambda code to send dlq messages to S3'
    # Upload Lambda Code
    cd ~
    mkdir app-awsevents-to-aes
    cp aws-events-to-elasticsearch/events-ingester-function/* app-awsevents-to-aes/
    cd app-awsevents-to-aes
    python -m venv eventsLambda
    source eventsLambda/bin/activate
    mv lambda_function.py eventsLambda/lib/python*/site-packages/
    mv requirements.txt eventsLambda/lib/python*/site-packages/
    cd eventsLambda/lib/python*/site-packages/
    pip install -r requirements.txt 
    deactivate
    mv ../dist-packages/* .
    zip -r9 eventsLambdaFunction.zip .
    aws s3 cp eventsLambdaFunction.zip s3://$BUCKET_NAME

else
  echo "Remind to create an environment variable for your bucket name."
fi