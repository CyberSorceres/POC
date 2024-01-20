import json
import logging
import boto3

from botocore.exceptions import ClientError


# Gestione degli errori ricevuti da BedRock
class ImageError(Exception):

    def __init__(self, message):
        self.message = message


# creazione dell'oggetto per il login che viene utilizzato per accedere a BedRock
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# generazione testo da parte di BedRock
def generate_text(model_id, body):
    """
    Input:
        model_id (str): L'ID del modello da utilizzare
        body (str) : La richiesta da fare al modello
    Returns:
        response (json): risposta del modello
    """

    logger.info(
        "Generating text with Titan Text G1 - Express model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Text generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated text with Titan Text G1 - Express model %s", model_id)

    return response_body


def lambda_handler(event, context):
    # print dell'event e salvataggio nella variabile user_prompt
    print(event)
    user_prompt = event['prompt']

    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        model_id = 'amazon.titan-text-express-v1'

        #        prompt = """Hello. """

        body = json.dumps({
            "inputText": user_prompt,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        })

        response_body = generate_text(model_id, body)
        print(f"Input token count: {response_body['inputTextTokenCount']}")

        # estrapolazione delle informazioni dalla risposta di BedRock
        for result in response_body['results']:
            # print del numero di token
            print(f"Token count: {result['tokenCount']}")

            # print del testo
            print(f"Output text: {result['outputText']}")
            # salvataggio del testo nella variabile response_body_string
            response_body_string = f"{result['outputText']}"

            # print della ragione del completamento
            print(f"Completion reason: {result['completionReason']}")

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))
    except ImageError as err:
        logger.error(err.message)
        print(err.message)

    else:
        print(
            f"Finished generating text with the Titan Text G1 - Express model {model_id}.")

    return {
        'statusCode': 200,
        'body': response_body_string
    }
