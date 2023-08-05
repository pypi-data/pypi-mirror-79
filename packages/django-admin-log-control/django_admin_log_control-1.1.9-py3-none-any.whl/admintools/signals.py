from .models import CustomModelAdmin
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.admin.models import LogEntry
import telebot
import os


@receiver(post_save, sender=LogEntry)
def bot_message(sender, instance, **kwargs):
    bot = telebot.TeleBot(os.getenv('TELEGRAM_LOG_BOT_TOKEN', None))
    chat_id = os.getenv('TELEGRAM_LOG_CHAT_ID', None)
    message = LogEntry.objects.first()
    try:
        bot.send_message(chat_id, str((message.user_id,
                                       message.content_type_id,
                                       message.object_id,
                                       message.object_repr,
                                       message.action_flag,
                                       message.change_message)))
    except:
        pass
