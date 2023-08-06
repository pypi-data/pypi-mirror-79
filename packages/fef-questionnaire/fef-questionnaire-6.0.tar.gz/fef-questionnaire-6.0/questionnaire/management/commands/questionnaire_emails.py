from __future__ import print_function
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        from ...emails import send_emails
        res = send_emails()
        if res:
            print(res)
