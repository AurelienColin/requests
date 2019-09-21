from datetime import datetime

from Rignak_Request.tor import renew_tor
from Rignak_Misc.print import print_remaining_time
from Rignak_Misc.TWRV import ThreadWithReturnValue as TWRV

TIMEOUT = 120
COUNT_BEFORE_SPAM = 24//2


def routing(function, urls, count_before_renew=COUNT_BEFORE_SPAM, timeout=TIMEOUT):
    request_number = len(urls)
    renew_tor()
    begin = datetime.now()

    threads = [None] * min(request_number, count_before_renew)
    currents_urls = [''] * min(request_number, count_before_renew)

    results = {}
    for i, url in enumerate(urls):
        threads[i % count_before_renew] = TWRV(target=function, args=(url,))
        threads[i % count_before_renew].start()
        currents_urls[i % count_before_renew] = url

        if (not i % count_before_renew or i == request_number - 1) and i:
            for url, thread in zip(currents_urls, threads):
                results[url] = thread.join(timeout=timeout)
            renew_tor()
            print_remaining_time(begin, i, request_number)

    return results
