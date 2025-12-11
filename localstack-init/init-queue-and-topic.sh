#!/bin/bash

export AWS_DEFAULT_REGION=sa-east-1

echo "MaDe WiTh LoVe iN Beeneu <3"
echo "--- Initializing SQS and SNS in $AWS_DEFAULT_REGION ---"

awslocal sqs create-queue --queue-name users-queue
awslocal sqs create-queue --queue-name statistics-queue

awslocal sqs create-queue --queue-name beeneu-response-queue

awslocal sns create-topic --name beeneu-topic

USERS_QUEUE_URL=$(awslocal sqs get-queue-url --queue-name users-queue --query 'QueueUrl' --output text)
USERS_QUEUE_ARN=$(awslocal sqs get-queue-attributes --queue-url "$USERS_QUEUE_URL" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

STATISTICS_QUEUE_URL=$(awslocal sqs get-queue-url --queue-name statistics-queue --query 'QueueUrl' --output text)
STATISTICS_QUEUE_ARN=$(awslocal sqs get-queue-attributes --queue-url "$STATISTICS_QUEUE_URL" --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

TOPIC_ARN=$(awslocal sns list-topics --query "Topics[?contains(TopicArn, 'beeneu-topic')].TopicArn" --output text)

# Fan-out

awslocal sns subscribe \
    --topic-arn "$TOPIC_ARN" \
    --protocol sqs \
    --notification-endpoint "$USERS_QUEUE_ARN"

awslocal sns subscribe \
    --topic-arn "$TOPIC_ARN" \
    --protocol sqs \
    --notification-endpoint "$STATISTICS_QUEUE_ARN"

echo "--- Infrastructure created ---"
echo "Topic ARN: $TOPIC_ARN"
echo "Users Queue URL: $USERS_QUEUE_URL"
echo "Statistics Queue URL: $STATISTICS_QUEUE_URL"
awslocal sqs get-queue-url --queue-name beeneu-response-queue
