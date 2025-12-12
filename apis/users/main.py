import sys
import signal
sys.path.append("../../")

from loguru import logger
from core.consumer import Consumer
from apis.users.repository import UserRepository
from apis.users.event_dispatcher import EventHandlers

# Queue URLs
QUEUE_URL = "http://localhost:4566/000000000000/users-queue"
RESPONSE_QUEUE_URL = "http://localhost:4566/000000000000/beeneu-response-queue"


def main():
    logger.info("[UsersAPI] Starting consumer...")
    
    repository = UserRepository()
    handlers = EventHandlers(repository=repository)
    
    EVENT_HANDLERS = {
        "REGISTER_USER_RPC": handlers.register_user_rpc,
        "LIST_USERS_RPC": handlers.list_users_rpc,
        "UPDATE_USER_RPC": handlers.update_user_rpc,
        "SEND_EMAIL": handlers.send_email,
    }
    
    consumer = Consumer(
        queue_url=QUEUE_URL,
        response_queue_url=RESPONSE_QUEUE_URL
    )
    
    running = True
    
    def signal_handler(sig, frame):
        nonlocal running
        logger.info("[UsersAPI] Shutting down consumer...")
        running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("[UsersAPI] Consumer started. Press Ctrl+C to stop.")
    
    while running:
        try:
            consumer.consume(EVENT_HANDLERS)
        except Exception as ex:
            logger.error(f"[UsersAPI] Error in consumer loop: {str(ex)}")
    
    logger.info("[UsersAPI] Consumer stopped.")


if __name__ == "__main__":
    main()
