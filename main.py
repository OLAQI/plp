from astrbot import create_plugin
from astrbot.types import MessageSession, Event

plugin = create_plugin("微信拍一拍回复", "v0.1")

# 使用字典存储每个用户的拍一拍次数
user_pat_counts = {}

@plugin.on_event(types=["EventPat"])  # 监听拍一拍事件
async def handle_pat(event: Event):

    # 确认是“我”被拍了
    if "我" in event.ctx.content:

        user_id = event.sender_id # 获取发送者的ID
        # 更新拍一拍次数
        if user_id not in user_pat_counts:
            user_pat_counts[user_id] = 0
        user_pat_counts[user_id] += 1

        # 根据次数回复不同内容
        count = user_pat_counts[user_id]
        if count == 1:
            reply_text = "别拍啦！"
        elif count == 2:
            reply_text = "哎呀，还拍呀，别闹啦！"
        elif count == 3:
            reply_text = "别拍我啦  你要做什么  不理你了"
        else:
            reply_text = "已宕机，请勿要，谢谢配合"
            user_pat_counts[user_id] = 0  # 重置计数器
            
        await event.reply(reply_text)
