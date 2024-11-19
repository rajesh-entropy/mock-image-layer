#!/bin/sh
echo "Configuring localstack components..."

readonly LOCALSTACK_URL=http://localhost:4566
export LOCALSTACK_URL

# Variables
REGION="ap-south-1"
AWS_ACCESS_KEY_ID="test"
AWS_SECRET_ACCESS_KEY="test"
AWS_PROFILE="localstack"


# DDB Tables
USER_IMAGES_TABLE="user-images"

# S3 Buckets
IMAGE_BUCKET_NAME="images.instagram.com"

export AWS_PROFILE=$AWS_PROFILE
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set region $REGION
aws configure set output json

# creating tables
aws dynamodb create-table \
  --table-name $USER_IMAGES_TABLE \
  --attribute-definitions AttributeName=user_id,AttributeType=S AttributeName=image_id,AttributeType=S\
  --key-schema AttributeName=user_id,KeyType=HASH AttributeName=image_id,KeyType=RANGE\
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --endpoint-url=$LOCALSTACK_URL \
  --no-cli-pager

# creating s3 buckets
aws s3api create-bucket --bucket $IMAGE_BUCKET_NAME \
  --endpoint-url $LOCALSTACK_URL \
  --create-bucket-configuration LocationConstraint=$REGION

# Sleep to let the index to get created
sleep 1
