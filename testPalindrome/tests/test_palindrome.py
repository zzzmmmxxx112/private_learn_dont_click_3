import pytest
from src.palindrome import (
    is_palindrome_simple,
    is_palindrome_ignore_case,
    is_palindrome_with_whitespace,
    is_palindrome_recursive,
    palindrome_stats
)


class TestPalindromeSimple:
    # 测试简单回文判断函数

    @pytest.mark.parametrize("text, expected", [
        # 基本回文测试
        ("racecar", True),
        ("level", True),
        ("deified", True),
        ("rotator", True),

        # 非回文测试
        ("hello", False),
        ("world", False),
        ("python", False),
        ("testing", False),

        # 边界情况
        ("a", True),
        ("", True),
        ("aa", True),
        ("ab", False),

        # 特殊字符
        ("12321", True),
        ("12345", False),
        ("@#@", True),
        ("@#%", False),

        # 大小写敏感测试
        ("Racecar", False),
        ("Level", False),
        ("Madam", False),
    ])
    def test_is_palindrome_simple(self, text, expected):
        # 测试基本回文判断
        result = is_palindrome_simple(text)
        assert result == expected, f"is_palindrome_simple('{text}') 应返回 {expected}"

    def test_is_palindrome_simple_invalid_input(self):
        # 测试无效输入类型
        with pytest.raises(TypeError):
            is_palindrome_simple(123)

        with pytest.raises(TypeError):
            is_palindrome_simple(None)

        with pytest.raises(TypeError):
            is_palindrome_simple([])


class TestPalindromeIgnoreCase:
    # 测试忽略大小写的回文判断

    @pytest.mark.parametrize("text, expected", [
        # 忽略大小写的回文
        ("Racecar", True),
        ("Level", True),
        ("Madam", True),
        ("A man a plan a canal Panama", False),  # 有空格，但不处理空格

        # 非回文
        ("Hello", False),
        ("World", False),

        # 边界情况
        ("A", True),
        ("a", True),
        ("", True),
        ("Aa", True),
        ("aA", True),
    ])
    def test_is_palindrome_ignore_case(self, text, expected):
        # 测试忽略大小写的回文判断
        result = is_palindrome_ignore_case(text)
        assert result == expected, f"is_palindrome_ignore_case('{text}') 应返回 {expected}"

    @pytest.mark.slow
    def test_is_palindrome_ignore_case_long_string(self):
        # 测试长字符串（性能测试）
        # 创建长回文字符串
        base = "abc" * 100
        long_palindrome = base + base[::-1]
        result = is_palindrome_ignore_case(long_palindrome)
        assert result is True


class TestPalindromeWithWhitespace:
    # 测试忽略空格和标点的回文判断

    @pytest.mark.parametrize("text, expected", [
        # 经典回文句子
        ("A man, a plan, a canal: Panama", True),
        ("Was it a car or a cat I saw?", True),
        ("No 'x' in Nixon", True),
        ("Eva, can I see bees in a cave?", True),

        # 非回文句子
        ("This is not a palindrome", False),
        ("Hello, world!", False),

        # 数字和符号
        ("12321", True),
        ("123 321", True),
        ("12:21", True),

        # 边界情况
        ("", True),
        ("a", True),
        (" ", True),
        ("  ", True),
    ])
    def test_is_palindrome_with_whitespace(self, text, expected):
        # 测试忽略空格和标点的回文判断
        result = is_palindrome_with_whitespace(text)
        assert result == expected, f"is_palindrome_with_whitespace('{text}') 应返回 {expected}"


class TestPalindromeRecursive:
    # 测试递归回文判断

    @pytest.mark.parametrize("text, expected", [
        ("racecar", True),
        ("hello", False),
        ("a", True),
        ("", True),
        ("abba", True),
        ("abcba", True),
    ])
    def test_is_palindrome_recursive(self, text, expected):
        # 测试递归回文判断
        result = is_palindrome_recursive(text)
        assert result == expected, f"is_palindrome_recursive('{text}') 应返回 {expected}"

    @pytest.mark.parametrize("invalid_input", [123, None, 3.14, [], {}])
    def test_is_palindrome_recursive_invalid_input(self, invalid_input):
        # 测试递归方法的无效输入
        with pytest.raises(TypeError):
            is_palindrome_recursive(invalid_input)


class TestPalindromeStats:
    # 测试回文统计函数

    def test_palindrome_stats_basic(self):
        # 测试基本回文统计
        result = palindrome_stats("racecar")
        assert result['original'] == "racecar"
        assert result['length'] == 7
        assert result['simple'] is True
        assert result['ignore_case'] is True
        assert result['with_whitespace'] is True
        assert result['recursive'] is True
        assert result['reversed'] == "racecar"
        assert result['is_empty'] is False
        assert result['is_single_char'] is False

    def test_palindrome_stats_sentence(self):
        # 测试句子回文统计
        result = palindrome_stats("A man, a plan, a canal: Panama")
        assert result['original'] == "A man, a plan, a canal: Panama"
        assert result['simple'] is False  # 大小写敏感
        assert result['ignore_case'] is False  # 有空格和标点
        assert result['with_whitespace'] is True  # 忽略空格和标点后是回文

    def test_palindrome_stats_empty(self):
       # 测试空字符串统计
        result = palindrome_stats("")
        assert result['length'] == 0
        assert result['simple'] is True
        assert result['is_empty'] is True
        assert result['is_single_char'] is False

    def test_palindrome_stats_single_char(self):
        # 测试单字符统计
        result = palindrome_stats("a")
        assert result['length'] == 1
        assert result['simple'] is True
        assert result['is_single_char'] is True
        assert result['is_empty'] is False

    @pytest.mark.parametrize("invalid_input", [123, None])
    def test_palindrome_stats_invalid_input(self, invalid_input):
        # 测试无效输入
        with pytest.raises(TypeError):
            palindrome_stats(invalid_input)


# 测试夹具示例
@pytest.fixture
def common_palindromes():
    # 提供常见回文字符串的夹具
    return ["racecar", "level", "radar", "civic", "madam"]


@pytest.fixture
def common_non_palindromes():
    # 提供常见非回文字符串的夹具
    return ["hello", "world", "python", "java", "testing"]


def test_with_fixtures(common_palindromes, common_non_palindromes):
    # 使用夹具的测试示例
    # 测试所有回文
    for text in common_palindromes:
        assert is_palindrome_simple(text) is True

    # 测试所有非回文
    for text in common_non_palindromes:
        assert is_palindrome_simple(text) is False


# 异常测试分组
@pytest.mark.exception
class TestExceptionCases:
    # 异常情况测试

    def test_type_error_for_int(self):
        # 测试整数输入引发TypeError
        with pytest.raises(TypeError, match="输入必须是字符串"):
            is_palindrome_simple(123)

    def test_type_error_for_list(self):
        # 测试列表输入引发TypeError
        with pytest.raises(TypeError, match="输入必须是字符串"):
            is_palindrome_simple([1, 2, 3])

    def test_type_error_for_none(self):
        # 测试None输入引发TypeError
        with pytest.raises(TypeError, match="输入必须是字符串"):
            is_palindrome_simple(None)


if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v"])