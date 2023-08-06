from .dialogue_manager import DialogueManager
from .task_engine import TaskEngine
from .knowledge_graph import KnowledgeGraph
from .question_answering import QuestionAnswering
from .intent_answering import IntentAnswering
from .ner_parser import NERParser
from .dialogue_act import DialogueAct
from .config_manager import ConfigManager
from .set import Set


class Bot:
    """
    机器人
    """

    def __init__(self, app_id, all_module=True, intent=False, qa=False, kg=False, te=False, dm=False, ner=False, act=False):
        self.app_id = app_id
        self.set = Set()
        if all_module or intent:
            self.intent = IntentAnswering(app_id, self.set)
        if all_module or qa:
            self.qa = QuestionAnswering(app_id, self.set)
        if all_module or kg:
            self.kg = KnowledgeGraph(app_id, self.set)
        if all_module or te:
            self.te = TaskEngine(app_id, self.set)
        if all_module or dm:
            self.dm = DialogueManager(app_id, self.set)
        if all_module or ner:
            self.ner = NERParser(app_id, self.set)
        if all_module or act:
            self.act = DialogueAct(app_id, self.set)
        self.config = ConfigManager(app_id, self.set)
