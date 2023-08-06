doc = """
                      cqh_psum
========


Usage
-----

Example
---------------------------
*  统计一个进程

 ``cqh_psum --name=python``

* 统计多个进程

  ``cqh_psum --name=python,coder,nginx``  

* 忽略某些进程

   ``cqh_psum --name=supervisor --exclude=supervisorctl,grep`` 

* 查看具体的进程

    ``cqh_psum --name=supervisor --show=1``

* and查新

    ``cqh_psum --name=supervisor__supervisorctl --show=1``

* 显示所有进程, 这个*是特殊处理的

  ``cqh_psum --name=* --show=1``

  






                      """
