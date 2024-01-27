from vertexai.language_models import CodeGenerationModel


def generate_a_function(temperature: float = 0.5) -> object:
    """Example of using Codey for Code Generation to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    code_generation_model = CodeGenerationModel.from_pretrained("code-bison@001")
    response = code_generation_model.predict(
        prefix="""not EXISTS how to use in sqlite3""", **parameters
    )

    print(f"Response from Model: {response.text}")

    return response


if __name__ == "__main__":
    generate_a_function()