@plugin.on_message(keywords=["拍了拍我"])
async def handle_pat(session: MessageSession):
    user_id = session.ctx.user_id  # 获取用户ID[<sup>2</sup>](https://github.com/Soulter/AstrBot/wiki/四、开发插件)[<sup>4</sup>](https://blog.51cto.com/u_15483555/13267318)
    
    # 初始化用户状态
    if user_id not in user_states:
        user_states[user_id] = 0
    user_states[user_id] += 1  # 计数器递增[<sup>2</sup>](https://github.com/Soulter/AstrBot/wiki/四、开发插件)

    # 根据次数返回不同响应
    count = user_states[user_id]
    if count == 1:
        await session.reply("别拍啦！")
    elif count == 2:
        await session.reply("哎呀，还拍呀，别闹啦！")
    elif count == 3:
        await session.reply("别拍我啦 你要做什么 不理你了")
    else:
        await session.reply("已宕机，请勿要，谢谢配合")
        user_states[user_id] = 0  # 重置计数器[<sup>2</sup>](https://github.com/Soulter/AstrBot/wiki/四、开发插件)
