# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('count', models.IntegerField(default=1, verbose_name='数量')),
                ('price', models.DecimalField(decimal_places=2, verbose_name='单价', max_digits=10)),
                ('comment', models.TextField(default='', verbose_name='评价信息')),
            ],
            options={
                'db_table': 'df_order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('order_id', models.CharField(serialize=False, max_length=64, primary_key=True, verbose_name='订单号')),
                ('total_count', models.IntegerField(default=1, verbose_name='商品总数')),
                ('total_amount', models.DecimalField(decimal_places=2, verbose_name='商品总金额', max_digits=10)),
                ('trans_cost', models.DecimalField(decimal_places=2, verbose_name='运费', max_digits=10)),
                ('pay_method', models.SmallIntegerField(default=1, choices=[(1, '货到付款'), (2, '支付宝')], verbose_name='支付方式')),
                ('status', models.SmallIntegerField(default=1, choices=[(1, '待支付'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '已完成')], verbose_name='订单状态')),
                ('trade_id', models.CharField(unique=True, max_length=100, blank=True, verbose_name='支付编号', null=True)),
            ],
            options={
                'db_table': 'df_order_info',
            },
        ),
    ]
