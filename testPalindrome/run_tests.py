import subprocess
import sys
import os
from datetime import datetime


def run_pylint():
    # 运行pylint代码质量检查
    print("=" * 60)
    print("运行 pylint 代码质量检查")
    print("=" * 60)

    files_to_check = ["src/palindrome.py", "tests/test_palindrome.py"]

    for file in files_to_check:
        if os.path.exists(file):
            print(f"\n检查文件: {file}")
            result = subprocess.run(
                ["pylint", "--rcfile=.pylintrc", file],
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.stderr:
                print("错误:", result.stderr)

            # 提取评分
            for line in result.stdout.split('\n'):
                if "Your code has been rated at" in line:
                    print(f"评分结果: {line}")
        else:
            print(f"文件不存在: {file}")


def run_pytest():
    # 运行pytest单元测试
    print("\n" + "=" * 60)
    print("运行 pytest 单元测试")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest",
         "--cov=src",
         "--cov-report=term-missing",
         "--cov-report=html:coverage_html",
         "--html=test_report.html",
         "--self-contained-html",
         "-v"],
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.stderr:
        print("错误输出:", result.stderr)

    # 生成详细覆盖率报告
    print("\n" + "=" * 60)
    print("生成详细覆盖率报告")
    print("=" * 60)
    subprocess.run([sys.executable, "-m", "coverage", "report", "-m"])

    return result.returncode


def generate_summary():
    # 生成测试摘要报告
    print("\n" + "=" * 60)
    print("测试摘要报告")
    print("=" * 60)
    print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n生成的报告:")
    print("1. test_report.html - pytest详细测试报告")
    print("2. coverage_html/ - 覆盖率HTML报告")
    print("3. pylint输出在控制台")


if __name__ == "__main__":
    print("开始执行回文测试项目...")

    # 1. 运行代码质量检查
    run_pylint()

    # 2. 运行单元测试
    exit_code = run_pytest()

    # 3. 生成摘要
    generate_summary()

    print("\n" + "=" * 60)
    print("测试执行完成!")
    print("=" * 60)
    sys.exit(exit_code)