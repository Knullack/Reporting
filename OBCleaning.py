from threading import Thread
from Chrome_Session import chromeSession
from time import sleep
import logging

def OBClean(list_containers: list) -> None:
    ports = [9222, 9223, 9224]
    threads = []
    sessions = []

    def thread_target(port, result_list):
        try:
            session = chromeSession('hdc3', 12730876, port)
            if session.driver:
                logging.info(f"Driver initialized for port {port}")
            else:
                logging.error(f"Driver not initialized for port {port}")
            result_list.append(session)  # Store the session object in the result list
        except Exception as e:
            logging.error(f"Error in thread with port {port}: {e}")

    # Start threads
    for port in ports:
        thread = Thread(target=thread_target, args=(port, sessions))
        threads.append(thread)
        thread.start()
        sleep(1)  # Delay to ensure each instance starts properly

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Process results
    for session in sessions:
        # Example processing of each session
        logging.info(f"Session with driver: {session.driver}")

    a = 0
    b = 0
    c = 0

OBClean(["csX1, csX2"])