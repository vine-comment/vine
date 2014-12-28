#!/usr/bin/env python
import os
import sys
import jieba
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vine_comment.settings")

    # Autoreloader will take a reload, so check it or it will run twice:
    # https://code.djangoproject.com/ticket/8085
    if os.environ.get('RUN_MAIN', False):
        if 'runserver' in sys.argv:
            if not jieba.initialized:
                jieba.initialize()
    execute_from_command_line(sys.argv)
