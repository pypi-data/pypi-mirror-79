# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from xyz_restful.mixins import IDAndStrFieldSerializerMixin
from rest_framework import serializers

from . import models


class TaskSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = (
            'title', 'content', 'is_active', 'is_force', 'link', 'target_user_tags', 'category', 'create_time',
            'is_sent', 'send_time', 'expiration'
        )


class MessageSerializer(IDAndStrFieldSerializerMixin, serializers.ModelSerializer):
    task = TaskSerializer()
    sender_name = serializers.CharField(label='发送者', source='sender.get_full_name', read_only=True)

    class Meta:
        model = models.Message
        fields = (
            'title', 'task', 'sender_name', 'sender', 'is_force', 'is_read', 'create_time', 'read_time', 'is_active',
            'expiration'
        )
        read_only_fields = ('sender', 'create_time')
