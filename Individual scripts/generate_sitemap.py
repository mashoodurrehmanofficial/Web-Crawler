import sys
import logging,requests
from pysitemap import crawler
root_url = 'https://pixinvent.com/materialize-material-design-admin-template/html/ltr/vertical-modern-menu-template/'
if __name__ == '__main__':
    if '--iocp' in sys.argv:
        from asyncio import events, windows_events
        sys.argv.remove('--iocp')
        logging.info('using iocp')
        el = windows_events.ProactorEventLoop()
        events.set_event_loop(el)

    # root_url = sys.argv[1] 
    crawler(root_url, out_file='sitemap.txt',out_format='txt')



 
def createsitemap():
    if '--iocp' in sys.argv:
        from asyncio import events, windows_events
        sys.argv.remove('--iocp')
        logging.info('using iocp')
        el = windows_events.ProactorEventLoop()
#         events.set_event_loop(el)
# from pysitemap import crawler
#     root_url = 'https://unityfreepaidassets.com/'
#     crawler(root_url, out_file='sitemap.txt',out_format='txt')
 