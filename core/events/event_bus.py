"""事件总线（预留拓展：解耦组件间通信）"""
import logging
from typing import Callable, Dict, List

class EventBus:
    """事件总线（单一职责：事件订阅/发布，解耦组件）"""
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        logging.info("【事件总线】初始化完成")

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """订阅事件（预留）"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
        logging.info(f"【事件总线】订阅事件 | 类型: {event_type} | 回调: {callback.__name__}")

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """取消订阅（预留）"""
        if event_type in self.subscribers and callback in self.subscribers[event_type]:
            self.subscribers[event_type].remove(callback)
            logging.info(f"【事件总线】取消订阅 | 类型: {event_type} | 回调: {callback.__name__}")

    def publish(self, event_type: str, **kwargs) -> None:
        """发布事件（预留）"""
        if event_type not in self.subscribers:
            return
        for callback in self.subscribers[event_type]:
            try:
                callback(** kwargs)
            except Exception as e:
                logging.error(f"【事件总线】事件处理失败 | 类型: {event_type} | 错误: {str(e)}")
        logging.info(f"【事件总线】发布事件 | 类型: {event_type} | 参数: {kwargs}")

# 全局事件总线实例（预留）
global_event_bus = EventBus()