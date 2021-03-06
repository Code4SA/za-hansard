import pprint
import httplib2
import re
import datetime
import time
import sys

from optparse import make_option
from bs4 import BeautifulSoup

from django.conf import settings


from django.core.management.base import BaseCommand, CommandError

from za_hansard.models import Source

class FailedToRetrieveSourceException (Exception):
    pass

class Command(BaseCommand):
    help = 'Check for new sources'
    option_list = BaseCommand.option_list + (
        make_option('--check-all',
            default=False,
            action='store_true',
            help="Don't stop when when reaching a previously seen item",
        ),
        make_option('--start-offset',
            default=0,
            type='int',
            help='Offset to start checking from',
        ),
        make_option('--limit',
            default=0,
            type='int',
            help='Limit last entry to check',
        ),
        make_option('--historical-limit',
            default='2009-04-22',
            type='str',
            help='Limit earliest historical entry to check (in yyyy-mm-dd format, default 2009-04-22)',
        ),
        make_option('--delete-existing',
            default=False,
            action='store_true',
            help='Delete existing sources (implies --check-all)',
        ),
    )

    def handle(self, *args, **options):

        if options['delete_existing']:
            Source.objects.all().delete()

        self.historical_limit = datetime.datetime.strptime(options['historical_limit'], '%Y-%m-%d').date()

        sources = self.retrieve_sources(options['start_offset'], options)
        sources.reverse()
        sources_db = [Source.objects.get_or_create(**source) for source in sources]
        sources_count = len(sources)
        created_count = sum([1 for (_,created) in sources_db if created])
        self.stdout.write('Sources found: %d\nSources created: %d\n' % (
            sources_count, created_count))

    def retrieve_sources(self, start, options):

        try:
            url = 'http://www.parliament.gov.za/live/content.php?Category_ID=119&DocumentStart=%d' % (start or 0)
            self.stdout.write("Retrieving %s\n" % url)
            h = httplib2.Http( settings.HTTPLIB2_CACHE_DIR )
            response, content = h.request(url)
            assert response.status == 200
            self.stdout.write("OK\n")
            # content = open('test.html').read()

            # parse content
            soup = BeautifulSoup(
                content,
                'xml',
            )

            rx = re.compile(r'Displaying (\d+)  (\d+) of the most recent (\d+)')

            pager = soup.find('td', text=rx)
            match = rx.search(pager.text)
            (pstart, pend, ptotal) = [int(p) for p in match.groups()]

            self.stdout.write( "Processing %d to %d\n" % (pstart, pend) )

            nodes = soup.findAll( 'a', text="View Document" )
            def scrape(node):
                url = node['href']
                table = node.find_parent('table')
                rx = re.compile(r'>([^:<]*) : ([^<]*)<')

                data = {}
                for match in re.finditer(rx, str(table)):
                    groups = match.groups()
                    data[groups[0]] = groups[1]

                title = ''
                try:
                    data['Title'] = table.find('b').text
                except:
                    data['Title'] = data.get('Document Summary', '(unknown)')

                try:
                    document_date = datetime.datetime.strptime(data['Date Published'], '%d %B %Y').date()
                except Exception as e:
                    raise CommandError( "Date could not be parsed\n%s" % str(e) )
                    # document_date = datetime.date.today()

                #(obj, created) = Source.objects.get_or_create(
                return {
                    'document_name':   data['Document Name'],
                    'document_number': data['Document Number'],
                    'defaults': {
                        'url':      url,
                        'title':    data['Title'],
                        'language': data.get('Language', 'English'),
                        'house':    data.get('House', '(unknown)'),
                        'date':     document_date,
                    }
                }
            scraped = []
            for node in nodes:
                s = scrape(node)
                if Source.objects.filter(
                    document_name   = s['document_name'],
                    document_number = s['document_number']).exists():
                    if not options['check_all']:
                        print "Reached seen document. Stopping.\n"
                        return scraped
                if s['defaults']['date'] < self.historical_limit:
                    print "Reached historical limit. Stopping.\n"
                    return scraped

                # otherwise
                scraped.append(s)

            if pend < (options['limit'] or ptotal):
                # NB following isn't phrased as a tail call, could rewrite if
                # that becomes important
                scraped = scraped + self.retrieve_sources(pend, options)
            return scraped

        except Exception as e:
            print >> sys.stderr, "ERROR: %s" % str(e)
            return []
