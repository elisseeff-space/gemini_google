import vertexai

PROJECT_ID = "ai-elis-project"
LOCATION = "us-central1" #e.g. us-central1

vertexai.init(project=PROJECT_ID, location=LOCATION)
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
)

from vertexai.preview.generative_models import (
    Content,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
)

model = GenerativeModel("gemini-pro")

responses = model.generate_content("Почему небо голубое?", stream=True)

final_response = ''
for response in responses:
    final_response += response.text
print(final_response)
print(responses)