from django.core.management.base import BaseCommand

from jobs.services import JoinSyncError, sync_join_jobs


class Command(BaseCommand):
    help = 'Sync job listings from JOIN into the local database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-missing',
            action='store_true',
            help='Do not delete local JOIN-synced jobs that are missing from JOIN.',
        )

    def handle(self, *args, **options):
        try:
            summary = sync_join_jobs(delete_missing=not options['keep_missing'])
        except JoinSyncError as exc:
            self.stderr.write(self.style.ERROR(str(exc)))
            return

        self.stdout.write(
            self.style.SUCCESS(
                'JOIN sync complete: '
                f"{summary['created_or_updated']} jobs synced, "
                f"{summary['deleted']} jobs deleted, "
                f"{summary['fetched']} jobs fetched."
            )
        )
