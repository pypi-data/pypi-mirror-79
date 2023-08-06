==============
pytest-change-report: pytest plugin
==============


**This pytest plugin turn . into √，turn F into x**


Usage
=====

从github源码安装

   pip install git+https://github.com/yoyoketang/pytest-change-report.git

命令行运行示例

   pytest --change on


demo
====

先写pytest用例test_demo.py

    def test_01():
        a = "hello"
        b = "hello"
        assert a == b


    def test_02(login):
        a = "hello"
        b = "hello world"
        assert a == b

命令行执行pytest, 默认不会改变之前的报告内容

    >pytest test_demo.py
    ============================= test session starts =============================
    collected 2 items

    test_demo.py .F                                                          [100%]

    ================================== FAILURES ===================================
    ___________________________________ test_02 ___________________________________

        def test_02():
            a = "hello"
            b = "hello world"
    >       assert a == b
    E       AssertionError: assert 'hello' == 'hello world'
    E         - hello
    E         + hello world

    test_demo.py:10: AssertionError
    ===================== 1 failed, 1 passed in 0.11 seconds ======================

加上 --change on 参数后运行

    >pytest test_demo.py --change on
    ============================= test session starts =============================
    collected 2 items

    test_demo.py √x                                                          [100%]

    ================================== FAILURES ===================================
    ___________________________________ test_02 ___________________________________

        def test_02():
            a = "hello"
            b = "hello world"
    >       assert a == b
    E       AssertionError: assert 'hello' == 'hello world'
    E         - hello
    E         + hello world

    test_demo.py:10: AssertionError
    ===================== 1 failed, 1 passed in 0.08 seconds ======================



pytest.ini
==========

可以添加到pytest.ini配置文件，这样默认就会带上--change参数

      [pytest]
      --change = on


