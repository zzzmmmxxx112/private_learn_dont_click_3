def is_palindrome_simple(text: str) -> bool:
    """
    简单判断是否为回文（区分大小写）
    Examples:
        >>> is_palindrome_simple("racecar")
        True
        >>> is_palindrome_simple("hello")
        False
    """
    if not isinstance(text, str):
        raise TypeError("输入必须是字符串")

    # 空字符串和单个字符都是回文
    if len(text) <= 1:
        return True

    # 使用切片反转字符串进行比较
    return text == text[::-1]


def is_palindrome_ignore_case(text: str) -> bool:
    # 忽略大小写判断是否为回文
    if not isinstance(text, str):
        raise TypeError("输入必须是字符串")

    # 转换为小写并移除空白
    cleaned = text.lower().strip()
    if len(cleaned) <= 1:
        return True

    return cleaned == cleaned[::-1]


def is_palindrome_with_whitespace(text: str) -> bool:
    # 忽略空格和标点判断是否为回文
    if not isinstance(text, str):
        raise TypeError("输入必须是字符串")

    import re
    # 只保留字母数字字符并转换为小写
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower())

    if len(cleaned) <= 1:
        return True

    return cleaned == cleaned[::-1]


def is_palindrome_recursive(text: str) -> bool:
    # 使用递归方法判断是否为回文
    if not isinstance(text, str):
        raise TypeError("输入必须是字符串")

    def _is_palindrome(s: str, start: int, end: int) -> bool:
        """递归辅助函数"""
        # 基本情况
        if start >= end:
            return True

        # 如果首尾字符相同，递归检查子串
        if s[start] == s[end]:
            return _is_palindrome(s, start + 1, end - 1)
        return False

    return _is_palindrome(text, 0, len(text) - 1)


def palindrome_stats(text: str) -> dict:
    # 获取字符串的回文统计信息
    if not isinstance(text, str):
        raise TypeError("输入必须是字符串")

    return {
        'original': text,
        'length': len(text),
        'simple': is_palindrome_simple(text),
        'ignore_case': is_palindrome_ignore_case(text),
        'with_whitespace': is_palindrome_with_whitespace(text),
        'recursive': is_palindrome_recursive(text),
        'reversed': text[::-1],
        'is_empty': len(text) == 0,
        'is_single_char': len(text) == 1
    }