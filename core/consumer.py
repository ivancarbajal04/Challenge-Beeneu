import json
import boto3
from typing import Dict, Any, Callable
from loguru import logger

# AWS LocalStack Configuration
AWS_REGION = 'sa-east-1'
ENDPOINT_URL = 'http://localhost:4566'
AWS_ACCESS_KEY = 'test'
AWS_SECRET_KEY = 'test'


class Consumer:
    def __init__(self, queue_url: str, response_queue_url: str = None):
        self.sqs = boto3.client(
            'sqs',
            region_name=AWS_REGION,
            endpoint_url=ENDPOINT_URL,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        
        self.queue_url = queue_url
        self.response_queue_url = response_queue_url
        
        self.MAX_NUMBER_MESSAGES = 10
        self.POLLING_TIME = 5



    def delete_message(self, receipt_handle: str):
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )



    def send_response(self, correlation_id: str, data: Any, status: str = "OK"):
        if not self.response_queue_url:
            logger.warning("No response queue URL configured")
            return
        
        response_message = {
            "correlation_id": correlation_id,
            "data": data,
            "status": status
        }
        
        self.sqs.send_message(
            QueueUrl=self.response_queue_url,
            MessageBody=json.dumps(response_message)
        )
        
        logger.success(f"Response sent - correlation_id: {correlation_id}")



    def _parse_message(self, body: Dict) -> Dict:
        
        if "Message" in body and isinstance(body["Message"], str):
            return json.loads(body["Message"])
        return body



    def consume(self, event_handlers: Dict[str, Callable]):
        try:
            result = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=self.MAX_NUMBER_MESSAGES,
                WaitTimeSeconds=self.POLLING_TIME
            )
            
            for message in result.get("Messages", []):
                receipt_handle = message["ReceiptHandle"]
                
                try:
                    body = json.loads(message["Body"])
                    
                    parsed = self._parse_message(body)
                    
                    event_type = parsed.get("event_type")
                    correlation_id = parsed.get("correlation_id")
                    payload = parsed.get("payload", {})
                    
                    logger.info(f"Message received - Event: {event_type} - Correlation ID: {correlation_id}")
                    
                    # execute the handler
                    handler = event_handlers.get(event_type)
                    
                    if handler:
                        response_data = handler(payload)
                        
                        if "_RPC" in event_type and self.response_queue_url:
                            self.send_response(correlation_id, response_data)
                    else:
                        logger.debug(f"No handler for event_type: {event_type}")
                    
                    self.delete_message(receipt_handle)
                    
                except json.JSONDecodeError as jex:
                    logger.error(f"Error decoding message: {str(jex)}")
                    self.delete_message(receipt_handle)
                except Exception as ex:
                    logger.error(f"Error processing message: {str(ex)}")
                    self.delete_message(receipt_handle)
                    
        except Exception as ex:
            import traceback
            logger.error(f"Consume error: {traceback.format_exc()}")