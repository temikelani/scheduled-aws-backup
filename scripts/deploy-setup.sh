#!/bin/bash -ex

# create-stack update-stack or delete-stack
COMMAND=$1 

# # set env variables
# chmod u+x ./scripts/set-env-variables.sh
# source ./scripts/set-env-variables.sh

# Path to template file
TEMPLATE="./0-setup/setup.yaml"

# Path to Parameters
# PARAMS="./0-setup-resources/parameters.json"

case $COMMAND in

  create-stack)
    aws cloudformation create-stack \
    --stack-name $STACK_NAME \
    --template-body file://$TEMPLATE \
    --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM" 

    sleep 100
    # upload date to s3 bucket
    aws s3 cp ./0-setup/order_data.csv s3://$BUCKET_NAME/ 
    ;;

  update-stack)
    aws cloudformation update-stack \
    --stack-name $STACK_NAME\
    --template-body file://$TEMPLATE \
    --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM" 
    ;;

  delete-stack)
    #empty s3 bucket
    aws s3 rm s3://$BUCKET_NAME --recursive

    aws cloudformation delete-stack \
    --stack-name $STACK_NAME
    ;;

  *)
    echo -n "Wrong arguments : Run script as follows:" 
    echo -n "Wrong arguments : ./run.sh arg1:" 
    echo -n "Where arg1: create-stack | update-stack | delete-stack"
    ;;
esac










# case $COMMAND in

#   create-stack)
#     aws cloudformation create-stack \
#     --stack-name $STACK_NAME \
#     --template-body file://$TEMPLATE \
#     --parameters file://$PARAMS \
#     --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM" 
#     ;;