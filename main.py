from astrbot.api.all import *
import time

@register("wechat_poke", "Your Name", "微信拍了拍回复", "1.0.1", "repo url") # 最好更新一个版本号
class WeChatPokePlugin(Star):

    def __init__(self, context: Context):
        super().__init__(context)
        # 使用字典记录每个用户的拍一拍次数, key: user_id, value: (timestamp, count)
        self.poke_counts = {}
        self.poke_responses = [
            "别拍啦！",
            "哎呀，还拍呀，别闹啦！",
            "别拍我啦  你要做什么  不理你了",
            "已宕机，请勿要，谢谢配合"
        ]

    @event_message_type(EventMessageType.ALL)  # 或根据需要使用 GROUP_MESSAGE / PRIVATE_MESSAGE
    async def on_message(self, event: AstrMessageEvent):
        raw_message = event.message_obj.raw_message

      
        if raw_message:
            try:
                message_type = raw_message.get("type")
                content = raw_message.get("content", "")  # 获取消息内容 (注意可能为空，所以给个默认值 "")
                to_wxid = raw_message.get("to_wxid")      # 被拍的用户的 wxid
                from_wxid = raw_message.get("from_wxid")

                # 判断条件：
                # 1. 是系统消息 (type="system")
                # 2. 消息内容包含 "拍了拍"
                # 3. 被拍的用户是机器人自己 (to_wxid == event.message_obj.self_id)
                if message_type == "system" and "拍了拍" in content and to_wxid == event.message_obj.self_id:

                    # 更新拍一拍次数
                    now = time.time()
                    if from_wxid in self.poke_counts:
                         last_time, count = self.poke_counts[from_wxid]
                         if now - last_time < 60:  # 60秒内的拍一拍算多次
                            count += 1
                         else:
                            count = 1  # 超过60秒，重置计数
                    else:
                        count = 1

                    self.poke_counts[from_wxid] = (now, count)

                    if count <= len(self.poke_responses):
                         response = self.poke_responses[count - 1]
                    else:
                        response = self.poke_responses[-1]  # 大于4次

                    await event.send(response) # 发送消息

            except Exception as e:
                self.logger.error(f"处理微信拍一拍消息出错: {e}")

