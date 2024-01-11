
from tsotsa import _ORKG
import argparse


def argsparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contribution", type=bool,
                        help="Create contributin", default=False)
    parser.add_argument("--comparison", type=bool,
                        default=False, help="create comparison")
    parser.add_argument(
        '--token', type=str, help="Token help to identify use who make the change in orkg system")

    parser.add_argument(
        '--json_path_contribution', type=str, help="Json template which help to create a contribution")

    parser.add_argument(
        '--comparison_folder_path', type=str, help="Folder path that contain a list of json file form for the comparison")
    args = parser.parse_args()
    return args


if __name__ == '__main__':

    args = argsparser()
    orkg = _ORKG()

    if args.contribution == True:
        args.comparison = False
        orkg.create_contribution(
            token=args.token, json_template=args.json_path_contribution)

    elif args.comparison == True:
        args.contribution = False
        orkg.create_dataframe_comparison(
            token=args.token, comparison_folder_path=args.comparison_folder_path)

    else:
        print("No Process running")
