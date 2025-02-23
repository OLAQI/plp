from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain
from typing import Dict, Any
class PatPlugin(Star):
    def __init__(self, context: Context, config: Dict[str, Any]):
        super().__init__(context)
        self.config = config
        self.pat_count: Dict[str, int] = {}  # 存储每个用户的拍了拍次数

    @filter.event_message_type(EventMessageType.PAT_MESSAGE)
    async def on_pat_message(self, event: AstrMessageEvent):
        """处理拍了拍我事件"""
        user_id = event.message_obj.sender.user_id
        if user_id not in self.pat_count:
            self.pat_count[user_id] = 0

        self.pat_count[user_id] += 1
        count = self.pat_count[user_id]

        if count == 1:
            reply = "别拍啦！"
        elif count == 2:
            reply = "哎呀，还拍呀，别闹啦！"
        elif count == 3:
            reply = "别拍我啦 你要做什么 不理你了"
        else:
            reply = "已宕机，请勿要，谢谢配合"

        await event.send([Plain(reply)])

    def reset_pat_count(self, user_id: str):
        """重置某个用户的拍了拍次数"""
        if user_id in self.pat_count:
            self.pat_count[user_id] = 0
