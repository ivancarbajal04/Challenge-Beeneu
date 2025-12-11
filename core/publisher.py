from uuid import uuid4
from loguru import logger
from typing import Dict, Any
import json, time, boto3


# AWS LocalStack Configuration demo
AWS_REGION = 'sa-east-1'
ENDPOINT_URL = 'http://localhost:4566'
AWS_ACCESS_KEY = 'test'
AWS_SECRET_KEY = 'test'

RESPONSE_QUEUE = "http://sqs.sa-east-1.localhost.localstack.cloud:4566/000000000000/beeneu-response-queue"
TOPIC_ARN = "arn:aws:sns:sa-east-1:000000000000:beeneu-topic"

def default_publisher_service() -> "Publisher":
    return Publisher(topic_arn=TOPIC_ARN, 
                     response_queue_url=RESPONSE_QUEUE)

class Publisher:
    def __init__(self, topic_arn: str, response_queue_url: str = None):
        self.sns = boto3.client(
            'sns',
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        
        self.sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        
        self.topic_arn = topic_arn
        self.response_queue_url = response_queue_url
        self.TIMEOUT = 10
        self.POLLING_TIME = 2
        self.MAX_MESSAGES = 10



    def publish(self, event_type: str, payload: Dict[str, Any]) -> Dict:
        correlation_id = str(uuid4())
        
        message = {
            "event_type": event_type,
            "correlation_id": correlation_id,
            "payload": payload
        }
        
        try:
            response = self.sns.publish(
                TopicArn=self.topic_arn,
                Message=json.dumps(message)
            )
            
            logger.success(f"Message published - Event: {event_type} - Correlation ID: {correlation_id}")
            
            return {
                "success": True,
                "correlation_id": correlation_id
            }
        except Exception as ex:
            logger.error(f"Error publishing message: {str(ex)}")
            return {
                "success": False,
                "error": str(ex)
            }



    def call_rpc(self, event_type: str, payload: Dict[str, Any]) -> Dict:
        if not self.response_queue_url:
            return {"success": False, "error": "No response queue URL configured"}
        
        correlation_id = str(uuid4())
        
        message = {
            "event_type": event_type,
            "correlation_id": correlation_id,
            "payload": payload
        }
        
        try:
            self.sns.publish(
                TopicArn=self.topic_arn,
                Message=json.dumps(message)
            )
            
            logger.success(f"RPC Message published - Event: {event_type} - Correlation ID: {correlation_id}")
        except Exception as ex:
            logger.error(f"Error publishing message: {str(ex)}")
            return {"success": False, "error": str(ex)}
        
        logger.info(f"Waiting for response - correlation_id: {correlation_id}")
        
        # Polling to wait for response
        return self._wait_for_response(correlation_id)



    def _wait_for_response(self, correlation_id: str) -> Dict:
        start_time = time.time()
        
        while time.time() - start_time < self.TIMEOUT:
            try:
                response = self.sqs.receive_message(
                    QueueUrl=self.response_queue_url,
                    MaxNumberOfMessages=self.MAX_MESSAGES,
                    WaitTimeSeconds=self.POLLING_TIME
                )
                
                for message in response.get("Messages", []):
                    receipt_handle = message["ReceiptHandle"]
                    
                    try:
                        body = json.loads(message["Body"])
                        msg_correlation_id = body.get("correlation_id")
                        
                        if msg_correlation_id == correlation_id:
                            self.sqs.delete_message(
                                QueueUrl=self.response_queue_url,
                                ReceiptHandle=receipt_handle
                            )
                            
                            logger.success(f"Response received - correlation_id: {correlation_id}")
                            
                            return {
                                "success": True,
                                "correlation_id": correlation_id,
                                "data": body.get("data"),
                                "status": body.get("status", "OK")
                            }
                    
                    except json.JSONDecodeError as jex:
                        logger.error(f"Error decoding message: {str(jex)}")
                        self.sqs.delete_message(
                            QueueUrl=self.response_queue_url,
                            ReceiptHandle=receipt_handle
                        )
                        
            except Exception as ex:
                logger.error(f"Polling error: {str(ex)}")
        
        logger.warning(f"Timeout waiting for response - correlation_id: {correlation_id}")
        return {
            "success": False,
            "error": f"Timeout after {self.TIMEOUT} seconds",
            "correlation_id": correlation_id
        }