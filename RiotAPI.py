from riotwatcher import RiotWatcher
from RiotConsts import API_KEY, REGION

watcher = RiotWatcher(API_KEY)
print(watcher.match.by_id(REGION, 4237338963))