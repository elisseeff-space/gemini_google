from vertexai.language_models import CodeGenerationModel


def complete_code_function(temperature: float = 0.2) -> object:
    """Example of using Codey for Code Completion to complete a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 64,  # Token limit determines the maximum amount of text output.
    }

    code_completion_model = CodeGenerationModel.from_pretrained("code-gecko@001")
    
    try: 
        response = code_completion_model.predict(
        prefix="not EXISTS how to use in sqlite3", **parameters
        )
        print(f"Response from Model: {response.text}")
    except Exception as e:
        print(e)

    #print(f"Response from Model: {response.text}")

    return response


if __name__ == "__main__":
    complete_code_function()