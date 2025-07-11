from typing import Optional, Type, Union, Dict, List
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun

import google.generativeai as genai
# from google.generativeai.types import Part

# Configure GenAI client (uses GOOGLE_API_KEY from env)
genai.configure(api_key="AIzaSyBZtlNTr1ZN35BLcMGJgrC3e248r8HWZPY")

class ImageCaption(BaseModel):
    query: str = Field(description="Input query to be answered from image.")


class ITT(BaseTool):
    name: str = "image_to_text"
    description: str = "A tool for captioning and conversing with image"
    args_schema: Type[BaseModel] = ImageCaption
    image_bytes: Optional[bytes] = None

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> Union[List[Dict], str]:
        try:
            # Fallback if query is empty
            query_text = query.strip() or "Describe this image."

            # Create model
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={
                    "temperature": 0.4,
                    "top_p": 1,
                    "top_k": 32,
                    "max_output_tokens": 4096,
                },
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
            )

            # Prepare input
            if self.image_bytes:
                image_part = {"mime_type": "image/png", "data": self.image_bytes}
                prompt_parts = [image_part, query_text]
            else:
                prompt_parts = [query_text]

            # Generate content
            response = model.generate_content(prompt_parts)
            return response.text

        except Exception as e:
            return repr(e)