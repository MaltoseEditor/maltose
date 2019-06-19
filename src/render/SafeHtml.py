class SafeHTML:
    """为Jinja2模板转换"""

    def __init__(self, data: str):
        self.data = data

    def __html__(self) -> str:
        return self.data
