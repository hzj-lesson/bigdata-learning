#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境自检脚本 check_env.py —— 大数据学习平台（v5.11.1）配套
运行：python check_env.py
一次输出 Java / Python / pandas / JDK / Spark / MySQL / Git / Docker 的安装与状态。

说明：
- 某项 ❌ 不代表不能学，下方「结论」会给达标线。
- MySQL 连接需要密码，脚本只验证客户端是否安装，连接请自行 mysql -u root -p。
- Windows 上若 python 命令不存在，请用 py 或 python3 运行本脚本。
"""
import os
import shutil
import subprocess
import sys


def run(cmd, timeout=20):
    """执行命令，返回 (成功?, 首行输出)"""
    try:
        out = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        text = (out.stdout + out.stderr).strip()
        first = text.splitlines()[0] if text else ""
        return out.returncode == 0, first
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def line(ok, name, info=""):
    mark = "✅" if ok else "❌"
    print(f"{mark} {name}: {info}")


def main():
    print("==== 大数据学习环境自检 ====")
    print("(某项 ❌ 不代表不能学，看下方「结论」)\n")

    # 1. Python 本体（Windows 可能没有 python，回退 python3）
    ok, ver = run("python --version")
    if not ok:
        ok, ver = run("python3 --version")
    if not ok:
        ok, ver = run("py --version")
    line(ok, "Python", ver)
    py_ok = ok

    # 2. pandas
    if py_ok:
        ok, ver = run('python -c "import pandas as pd; print(pd.__version__)"')
        if not ok:
            ok, ver = run('python3 -c "import pandas as pd; print(pd.__version__)"')
        line(ok, "pandas", ("v" + ver) if ok else "未安装（pip install pandas）")

    # 3. JDK
    ok, ver = run("java -version")
    line(ok, "JDK", ver if ok else "未安装（装 Adoptium Temurin 17 并配 JAVA_HOME）")
    jh = os.environ.get("JAVA_HOME", "")
    line(bool(jh), "JAVA_HOME", jh if jh else "未设置（建议指向 JDK 安装目录）")

    # 4. Spark（pyspark 本地模式）
    ok, ver = run("pyspark --version")
    line(ok, "Spark(pyspark)", ver if ok else "未安装（或用 Docker 镜像绕过）")

    # 5. MySQL 客户端
    ok, ver = run("mysql --version")
    line(ok, "MySQL 客户端", ver if ok else "未安装（或用 SQLite 备胎）")
    print("   · MySQL 连接测试需密码，请自行运行：mysql -u root -p")

    # 6. Git
    ok, ver = run("git --version")
    line(ok, "Git", ver if ok else "未安装")

    # 7. Docker
    ok, ver = run("docker --version")
    line(ok, "Docker", ver if ok else "未安装（Windows 需开启 WSL2 后端）")

    print("\n==== 结论 ====")
    print("达标线：Python ✅ + pandas ✅ + JDK ✅ + Git ✅ 即可开始正课。")
    print("Spark / Docker 是进阶项，用 Spark 本地模式或 Docker 一键容器即可补足，")
    print("不必在「搭集群」上耗时间——环境是手段，不是目的。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消")
        sys.exit(1)
