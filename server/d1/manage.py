#!/usr/bin/env python
import os
import sys
import jieba

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d1.settings")

    from django.core.management import execute_from_command_line

    jieba.initialize()
    execute_from_command_line(sys.argv)
