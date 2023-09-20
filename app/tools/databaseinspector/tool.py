from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from langchain.chat_models.base import BaseChatModel
from langchain.prompts.chat import SystemMessagePromptTemplate
from langchain.tools.base import BaseTool, StructuredTool

from .prompt import default_help_prompt

from langchain.callbacks.manager import (
    AsyncCallbackManagerForChainRun,
    CallbackManagerForChainRun,
)

class VerifyDatabaseToolInput(BaseModel):
    # """Input for VerifyDatabaseTool"""
    lesson: str = Field(..., description="The URL of the lesson", example="neo4j://127.0.0.1:7687")
    uri: str = Field(..., description="URI of the database", example="neo4j://127.0.0.1:7687")
    username: str = Field(..., description="Username for database authentication", example="neo4j")
    password: str = Field(..., description="Password for database authentication", example="what-three-words")



class DatabaseInspectorTool(BaseTool):
    """
    Validate that a user has passed a hands-on code challenge.
    """

    name: str = "verify_database"
    description: str = """
    Verify that a user has completed the step to pass a hands-on code challenge lesson on GraphAcademy.

    Useful when the user is asking why they haven't completed the lesson,
    to verify the database, or why the verify button isn't working.

    Example questions:
    * why doesn't my database pass the validation?
    * why haven't I passed the lesson?
    * what is wrong with my database?
    """

    args_schema = VerifyDatabaseToolInput
    llm: Optional[BaseChatModel]
    help_prompt: SystemMessagePromptTemplate = default_help_prompt


    @staticmethod
    def with_llm(llm: BaseChatModel, help_prompt: SystemMessagePromptTemplate = default_help_prompt):
        cls = DatabaseInspectorTool()
        cls.llm = llm
        cls.help_prompt = help_prompt

        return cls

    # def __init__(self, llm: BaseChatModel, help_prompt: SystemMessagePromptTemplate = default_help_prompt):
    #     self.llm = llm
    #     self.help_prompt = help_prompt


    def _run(self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None):

        print(inputs)

        return 'hello'

    def _arun(self,
        inputs: Dict[str, Any],
        run_manager: Optional[AsyncCallbackManagerForChainRun] = None):
        raise NotImplementedError('Maybe one day')
