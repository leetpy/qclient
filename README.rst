Usage
=====

说明
----

使用前需要先配置认证信息，默认先读取 `~/.qingcloud/config.yaml` 文件，如果该文件不存在，
则读取工程目录下的 `config.yaml`.

查看帮助信息
------------

.. code-block:: console

    $ ./main.py -help
    usage: qingcloud client [-h]
                            {terminate-instances,run-instances,describe-instances}
                            ...
    
    positional arguments:
      {terminate-instances,run-instances,describe-instances}
        terminate-instances
                            terminate instances
        run-instances       create instances
        describe-instances  describe instances
    
    optional arguments:
      -h, --help            show this help message and exit



创建实例
--------

.. code-block:: console

    $ ./main.py run-instances -m centos73x64 --cpu 1 --memory 1024 -l passwd -p TestVM123456

查找实例
--------

.. code-block:: console

    $ ./main.py describe-instances -i i-uwlgvdc3,i-fulc7cdx

删除实例
--------

.. code-block:: console

    $ ./main.py terminate-instances -i i-uwlgvdc3
