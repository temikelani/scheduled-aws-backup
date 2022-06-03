#!/bin/bash -ex

# create-stack update-stack or delete-stack
COMMAND=$1 

case $COMMAND in

  update-stack)
    source ./scripts/deploy-setup.sh create-stack

    # Path to template file
    TEMPLATE="./1-cloudformation/on-demand-aws-backup-ddb-table.yaml"

    # Path to Parameters
    PARAMS="./1-cloudformation/on-demand-aws-backup-parameters.json"

    aws cloudformation update-stack \
    --stack-name $STACK_NAME\
    --template-body file://$TEMPLATE \
    --parameters file://$PARAMS \
    --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM" 
    ;;

  delete-stack)

    # Path to template file
    TEMPLATE="./1-cloudformation/on-demand-aws-backup-ddb-table.yaml"

    #empty s3 bucket
    aws s3 rm s3://$BUCKET_NAME --recursive

    aws cloudformation delete-stack \
    --stack-name $STACK_NAME
    ;;

  *)
    echo -n "Wrong arguments : Run script as follows:" 
    echo -n "Wrong arguments : ./run.sh arg1:" 
    echo -n "Where arg1: update-stack | delete-stack"
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