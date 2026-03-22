import logging
import logging.handlers


def setup_event_logging(app_name="MyPythonApp"):
    """配置logging模块使用Windows事件日志"""

    # 创建logger
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)

    # 移除所有已有的handler
    logger.handlers = []

    try:
        # 创建NTEventLogHandler
        handler = logging.handlers.NTEventLogHandler(app_name)

        # 设置日志格式
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        # 添加到logger
        logger.addHandler(handler)

        return logger
    except Exception as e:
        print(f"创建事件日志处理器失败: {e}")
        # 如果失败，回退到标准输出
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger


# 使用示例
logger = setup_event_logging("ClockForClassroom")
