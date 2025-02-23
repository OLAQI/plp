from astrbot import Bot, Plugin
from astrbot.store import DictStore

class WechatPatPlugin(Plugin):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.store = DictStore("wechat_pat_counts")  # 使用内置持久化存储[<sup>2</sup>](https://github.com/Soulter/AstrBot/wiki/四、开发插件)[<sup>4</sup>](https://blog.51cto.com/u_15483555/13267318)
    
    async def handle_pat(self, event):
        user_id = event.user_id
        count = await self.store.get(user_id, 0) + 1
        
        replies = [
            "别拍啦！",
            "哎呀，还拍呀，别闹啦！",
            "别拍我啦  你要做什么  不理你了",
            "已宕机，请勿要，谢谢配合"
        ]
        
        response = replies[min(count-1, 3)]  # 取前四次响应规则[<sup>1</sup>](https://astrbot.app/)
        await self.send(event, response)
        await self.store.set(user_id, count if count < 4 else 4)  # 计数上限设为4

def setup(bot):
    bot.register_plugin(WechatPatPlugin(bot))  # 注册插件[<sup>2</sup>](https://github.com/Soulter/AstrBot/wiki/四、开发插件)[<sup>5</sup>](https://blog.csdn.net/puterkey/article/details/145337107)
