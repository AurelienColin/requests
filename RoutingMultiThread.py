from datetime import datetime
import threading
import time

from Rignak_Misc.print import print_remaining_time
from Rignak_Misc.TWRV import ThreadWithReturnValue


def routing(function, urls, thread_limit=20, single_wait=0, printing=True, time_limit=10, time_sleep=10):
    thread_limit += threading.active_count()
    request_number = len(urls)
    begin = datetime.now()
    p = 0.0
    threads = []
    if printing:
        print(f'Begin at {begin.strftime("%H:%M")} for {len(urls)} request')
    try:
        for i, url in enumerate(urls):
            while threading.active_count() > thread_limit:
                time.sleep(0.01)
            threads.append(ThreadWithReturnValue(target=function, args=(url,)))
            threads[-1].start()

            if printing and p != int(i / request_number * 1000):
                print_remaining_time(begin, i, request_number)
                p = int(i / request_number * 1000)
            time.sleep(single_wait)
        time.sleep(time_sleep)
    except Exception as e:
        print(f'\nError: {url} because of "{e}"')

    threads = [thread.join(timeout=time_limit) for thread in threads]
    results = {url: thread for url, thread in zip(urls, threads) if thread is not None}
    return results
