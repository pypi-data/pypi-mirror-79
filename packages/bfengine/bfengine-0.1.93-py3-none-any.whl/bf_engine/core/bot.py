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

    def __init__(self, app_id, intent=False, qa=False, kg=False, te=False, dm=False, ner=False, act=False):
        self.app_id = app_id
        self.set = Set()
        if intent:
            self.intent = IntentAnswering(app_id, self.set)
        if qa:
            self.qa = QuestionAnswering(app_id, self.set)
        if kg:
            self.kg = KnowledgeGraph(app_id, self.set)
        if te:
            self.te = TaskEngine(app_id, self.set)
        if dm:
            self.dm = DialogueManager(app_id, self.set)
        if ner:
            self.ner = NERParser(app_id, self.set)
        if act:
            self.act = DialogueAct(app_id, self.set)
        self.config = ConfigManager(app_id, self.set)
