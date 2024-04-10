from config import Config
from map import DatabaseDocumentMap
from api.linebot_helper import LineBotHelper, QuickReplyHelper
from linebot.v3.messaging import (
    TextMessage,
    FlexMessage,
    FlexContainer
)
from abc import ABC, abstractmethod

config = Config()
firebaseService = config.firebaseService

class Template(ABC):
    @abstractmethod
    def execute(self, event):
        pass

class TemplateFactory:
    def __init__(self):
        self.template_map = {
            'course': Course,
            'certificate': Certificate
        }

    def get_template(self, task_name):
        template_class = self.template_map.get(task_name)
        if template_class:
            return template_class
        else:
            print("找不到對應的模板")
            return None

class Course(Template):
    """
    開課時間查詢
    """
    def execute(self, event):
        quick_reply_data = firebaseService.get_data('quick_reply', DatabaseDocumentMap.QUICK_REPLY.get("course").get("semester"))
        LineBotHelper.reply_message(event, [TextMessage(text=quick_reply_data.get('text'), quick_reply=QuickReplyHelper.create_quick_reply(quick_reply_data.get('actions')))])

class Certificate(Template):
    """
    證書申請流程
    """
    def execute(self, event):
        line_flex_str = firebaseService.get_data('line_flex', DatabaseDocumentMap.LINE_FLEX.get("certificate").get("carousel")).get('flex')
        LineBotHelper.reply_message(event, [FlexMessage(alt_text='證書申請流程', contents=FlexContainer.from_json(line_flex_str))])    