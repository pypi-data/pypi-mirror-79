========
pyfs-pay
========

Feishu Pay Module for Python.

Installation
============

::

    pip install pyfs-pay


Usage
=====

::

    from pyfs_pay import Pay, check_user_paid_scope


Method
======

::

    class Pay(TenantAccessToken):
        def __init__(self, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):
            super(Pay, self).__init__(appid=appid, secret=secret, ticket=ticket, tenant_key=tenant_key, token=token, storage=storage)

        def check_user_paid_scope(self, open_id=None, user_id=None, appid=None, secret=None, ticket=None, tenant_key=None, token=None, storage=None):

