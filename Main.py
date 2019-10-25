import argparse
import sys
from Riot.RiotAPI import *
from DTO.Match import Match


def main():
    # initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--matchid", type=int)

    # read arguments from the command line
    args = parser.parse_args()

    if args.matchid:
        match_id = args.matchid
        print('Match ID input - %s' % match_id)
    else:
        print('Match ID is required (--matchid)')
        sys.exit(0)

    # Riot API
    match = Match(match_id)
    fetch_match_stats(match)
    print(match.format_game_duration())



if __name__ == "__main__":
    main()