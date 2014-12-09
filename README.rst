============================
redis point-in-time recovery
============================

准备工作
========

* 用supervisor运行 ``set_redis_timestamp_key.py`` ，会自动每秒设置时间戳，需要在里面配置支持的redis地址列表，可在局域网任何一台机器运行。
* 每天午夜运行 ``backup_and_rewriteaof.py`` ，为每个redis实例运行一次，需要和redis相同机器运行，会自动备份aof文件并执行 ``bgrewriteaof`` 。

执行恢复
========

* redis停服，备份原redis数据目录，并用新的空数据目录启动redis。
* 执行 ``build_recovery_aof.py ... --timestamp xxx`` 按照需要的时间戳生成恢复用的 aof 文件。
* 对新启动的空redis进行数据恢复 ``cat recovery.aof | redis-cli --pipe --h redis_host --p redis_port``
