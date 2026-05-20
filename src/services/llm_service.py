from resources import llm_resources as llm_res
import json
import requests as rq
from app_log import logger
import time

def chat_with_llm(model, messages):
    logger.info("Sending request to LLM")
    start = time.time()
    try:
        payload = {
            "model" : model,
            "messages" : messages,
            "stream" : True
        }

        response = rq.post(url=llm_res.llm_chat_url, stream=True, json=payload, timeout=15)

        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line.decode("utf-8"))
            text = chunk.get("message", {}).get("content", "")
            yield text
        duration = time.time() - start
        logger.info(f"LLM response: {duration:.2f}s")
    except rq.exceptions.ConnectionError as e:
        logger.error(f"Model is not responsive: {e}")
        print(f"Model is not responsive: {e}")
    except rq.exceptions.ConnectTimeout as e:
        logger.error(f"Model took long time to respond: {e}")
        print(f"Model took long time to respond: {e}")
    except rq.exceptions.HTTPError as e:
        logger.error(f"Error establishing connection: {e}")
        print(f"Error establishing connection: {e}")
    except rq.exceptions.JSONDecodeError as e: 
        logger.error(f"The response was not valid JSON: {e}")
        print(f"The response was not valid JSON: {e}")
    except rq.exceptions.RequestException as e:
        logger.error(f"Some other request error happened: {e}")
        print(f"Some other request error happened: {e}")
    except Exception as e:
        logger.error(f"Exception occured: {e}")
        print(f"Exception occured: {e}")
