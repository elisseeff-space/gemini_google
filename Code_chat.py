import vertexai
import vertexai.preview
from vertexai.language_models import CodeChatModel
from google.cloud import aiplatform_v1


def write_a_function(temperature: float = 0.5) -> object:
    """Example of using Codey for Code Chat Model to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    }

    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    chat = code_chat_model.start_chat()

    response = chat.send_message(
        #"Please help write a function to calculate the min of two numbers", **parameters
        #"Write a function that checks if a year is a leap year.", **parameters
        #"Why the sky is blue?", **parameters
        """not EXISTS how to use in sqlite3""", **parameters
    )
    print(f"Response from Model: {response.text}\n")

    return response


if __name__ == "__main__":
    write_a_function()