import sys
import signal
sys.path.append("../../")

from loguru import logger
from core.consumer import Consumer
from event_dispatcher import EVENT_HANDLERS


# Queue URLs
QUEUE_URL = "http://localhost:4566/000000000000/statistics-queue"
RESPONSE_QUEUE_URL = "http://localhost:4566/000000000000/beeneu-response-queue"


def main():
    logger.info("[StatisticsAPI] Starting consumer...")
    
    consumer = Consumer(
        queue_url=QUEUE_URL,
        response_queue_url=RESPONSE_QUEUE_URL
    )
    
    running = True
    
    def signal_handler(sig, frame):
        nonlocal running
        logger.info("[StatisticsAPI] Shutting down consumer...")
        running = False
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("[StatisticsAPI] Consumer started. Press Ctrl+C to stop.")
    
    while running:
        try:
            consumer.consume(EVENT_HANDLERS)
        except Exception as ex:
            logger.error(f"[StatisticsAPI] Error in consumer loop: {str(ex)}")
    
    logger.info("[StatisticsAPI] Consumer stopped.")


if __name__ == "__main__":
    main()
