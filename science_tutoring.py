from vertexai.language_models import ChatModel, InputOutputTextPair


def science_tutoring(temperature: float = 0.2) -> None:
    chat_model = ChatModel.from_pretrained("chat-bison@001")

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    chat = chat_model.start_chat(
        context="My name is Miles. You are an astronomer, knowledgeable about the solar system.",
        examples=[
            InputOutputTextPair(
                input_text="How many moons does Neptune have?",
                output_text="Neptune, the eighth planet in our solar system, has 14 known moons to date. These moons range in size and composition, with the largest and most well-known being Triton. Triton is the seventh-largest moon in the solar system and is noteworthy for its retrograde orbit, meaning it orbits Neptune in the opposite direction to the planet's rotation. Other notable moons of Neptune include Nereid, Proteus, and Larissa. It's worth noting that new moons are occasionally discovered through observations and technological advancements, so the number of known moons around Neptune may increase in the future.",
            ),
            InputOutputTextPair(
                input_text="How many moons does Mars have?",
                output_text="The planet Mars has two moons, Phobos and Deimos.",
            ),
            InputOutputTextPair(
                input_text="What do you think about endless space?",
                output_text="Endless space, often referred to as the universe, is a subject that has fascinated humans for centuries. It raises questions about the vastness, mystery, and possibilities that lie beyond our planet Earth. Here are a few common thoughts and considerations related to endless space: 1. Exploration and Discovery: The idea of endless space captivates our imagination and fuels our desire to explore what lies beyond our current understanding. It presents opportunities to discover new celestial bodies, phenomena, and potentially even life forms..",
            ),
        ],
    )

    response = chat.send_message(
        #"How many planets are there in the solar system?", **parameters
        "What do you think about endless space?", **parameters
    )
    print(f"Response from Model: {response.text}")

    return response


if __name__ == "__main__":
    science_tutoring()