from typing import Union, Awaitable, List, Optional, ClassVar
from astrbot.core.message.components import BaseMessageComponent
from astrbot.core.message.message_event_result import MessageChain
from astrbot.api.platform import MessageMember, AstrBotMessage
from astrbot.core.platform.astr_message_event import MessageSesion
from astrbot.core.star.context import Context


class StarTools:
    """
    提供给插件使用的便捷工具函数集合
    这些方法封装了一些常用操作，使插件开发更加简单便捷!
    """

    _context: ClassVar[Optional[Context]] = None

    @classmethod
    def initialize(cls, context: Context) -> None:
        """
        初始化StarTools，设置context引用

        Args:
            context: 暴露给插件的上下文
        """
        cls._context = context

    @classmethod
    async def send_message(
        cls, session: Union[str, MessageSesion], message_chain: MessageChain
    ) -> bool:
        """
        根据session(unified_msg_origin)主动发送消息

        Args:
            session: 消息会话。通过event.session或者event.unified_msg_origin获取
            message_chain: 消息链

        Returns:
            bool: 是否找到匹配的平台

        Raises:
            ValueError: 当session为字符串且解析失败时抛出

        Note:
            qq_official(QQ官方API平台)不支持此方法
        """
        return await cls._context.send_message(session, message_chain)

    @classmethod
    async def create_message(
        cls,
        type: str,
        self_id: str,
        session_id: str,
        message_id: str,
        sender: MessageMember,
        message: List[BaseMessageComponent],
        message_str: str,
        raw_message: object,
        group_id: str = "",
    ):
        """
        创建一个AstrBot消息对象

        Args:
            type (str): 消息类型
            self_id (str): 机器人自身ID
            session_id (str): 会话ID(通常为用户ID)(QQ号, 群号等)
            message_id (str): 消息ID
            sender (MessageMember): 发送者信息
            message (List[BaseMessageComponent]): 消息组件列表
            message_str (str): 消息字符串
            raw_message (object): 原始消息对象
            group_id (str, optional): 群组ID, 如果为私聊则为空. Defaults to "".

        Returns:
            AstrBotMessage: 创建的消息对象
        """
        abm = AstrBotMessage()
        abm.type = type
        abm.self_id = self_id
        abm.session_id = session_id
        abm.message_id = message_id
        abm.sender = sender
        abm.message = message
        abm.message_str = message_str
        abm.raw_message = raw_message
        abm.group_id = group_id
        return abm

    # todo: 添加构造事件的方法
    # async def create_event(
    #     self, platform: str, umo: str, sender_id: str, session_id: str
    # ):
    #     platform = self._context.get_platform(platform)

    # todo: 添加找到对应平台并提交对应事件的方法

    @classmethod
    def activate_llm_tool(cls, name: str) -> bool:
        """
        激活一个已经注册的函数调用工具
        注册的工具默认是激活状态

        Args:
            name (str): 工具名称
        """
        return cls._context.activate_llm_tool(name)

    @classmethod
    def deactivate_llm_tool(cls, name: str) -> bool:
        """
        停用一个已经注册的函数调用工具

        Args:
            name (str): 工具名称
        """
        return cls._context.deactivate_llm_tool(name)

    @classmethod
    def register_llm_tool(
        cls, name: str, func_args: list, desc: str, func_obj: Awaitable
    ) -> None:
        """
        为函数调用（function-calling/tools-use）添加工具

        Args:
            name (str): 工具名称
            func_args (list): 函数参数列表
            desc (str): 工具描述
            func_obj (Awaitable): 函数对象，必须是异步函数
        """
        cls._context.register_llm_tool(name, func_args, desc, func_obj)

    @classmethod
    def unregister_llm_tool(cls, name: str) -> None:
        """
        删除一个函数调用工具
        如果再要启用，需要重新注册

        Args:
            name (str): 工具名称
        """
        cls._context.unregister_llm_tool(name)
