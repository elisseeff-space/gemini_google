PROJECT_ID = "'ai-elis-project'"
LOCATION = "us-central1" #e.g. us-central1

import vertexai
vertexai.init(project=PROJECT_ID, location=LOCATION)
from vertexai.preview.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
# Restart kernel after installs so that your environment can access the new packages
import IPython
import time

app = IPython.Application.instance()
app.kernel.do_shutdown(True)