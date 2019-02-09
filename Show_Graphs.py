from bokeh.plotting import figure, output_file, show
from sources.files_io import load_data_from_file
from sources.api_imdb import API_IMDb
from utylities.utylities import prepare_data_for_presentation, normalize_data, retrive_id_from_link
from collections import OrderedDict
import argparse
import sys

def create_graph(show_id, save, normalize, load_file, data, average, tv_show):
    """
    Creates graph from given arguments
    """
    # Passing it as an argument drastically shorten the run time
    imdb_api = tv_show
    
    reviews_raw = None
    votes_raw = None

    # Loading reviews options
    if load_file and 'r' in data:
        # Load reviews from file and set data range as 0-11
        reviews_raw = load_data_from_file('reviews', show_id)
        data_range = (0, 11)

        # Prepare data for presentation
        reviews_prepared = prepare_data_for_presentation(reviews_raw)

        # Set labels
        labels = list(reviews_prepared.keys())
    elif 'r' in data:
        # Load reviews from imdb and set data range as 0-11
        reviews_raw = imdb_api.download_reviews(save)
        data_range = (0, 11)

        # Prepare data for presentation
        reviews_prepared = prepare_data_for_presentation(reviews_raw)

        # Set labels
        labels = list(reviews_prepared.keys())

    # Loading number of votes options
    if load_file and 'v' in data:
        # Load votes from file and set data range as 0-max value
        votes_raw = load_data_from_file('votes', show_id)
        
        # Prepare votes for presentation
        votes_prepared = prepare_data_for_presentation(votes_raw)
        
        # Set labels
        labels = list(votes_prepared.keys())
        
        # Set data range as 0-max value + 10% of max value
        data_range = (0, max(votes_prepared.values()) + (0.1*max(votes_prepared.values())))
    elif 'v' in data:
        # Load votes from file and set data range as 0-max value
        votes_raw = imdb_api.download_number_of_votes(save)
        
        # Prepare votes for presentation
        votes_prepared = prepare_data_for_presentation(votes_raw)
        
        # Set labels
        labels = list(votes_prepared.keys())

        # Set data range as 0-max value + 10% of max value
        data_range = (0, max(votes_prepared.values()) + (0.1*max(votes_prepared.values())))

    # Normalize data if needed and set new data range
    if normalize and not votes_raw is None:
        votes_prepared = normalize_data(votes_prepared)
        data_range = (0, 11)
    
    # Create graph object
    p = figure(x_range=labels, y_range=data_range, sizing_mode='stretch_both', title=imdb_api.name)
    
    # Title location
    p.title_location = 'above'

    # Rotate axis, in radian PI/4 == 45*
    p.xaxis.major_label_orientation = 3.14/4

    # Add reviews lines
    if not reviews_raw is None:
        p.line(labels, list(reviews_prepared.values()), line_width=2, legend='Reviews', muted_alpha=0.1)

        if average:
            # Calculate average review value
            average_review = sum(reviews_prepared.values())/len(reviews_prepared.values())
            
            p.line(labels, average_review, line_width=1, legend='Average review', line_color='black', muted_alpha=0.1)

    # Add number of votes lines
    if not votes_raw is None:
        p.line(labels, list(votes_prepared.values()), line_width=2, legend='Number of votes', line_color='red', muted_alpha=0.1)

        if average:
            # Calculate average review value
            average_votes = sum(votes_prepared.values())/len(votes_prepared.values())
            
            p.line(labels, average_votes, line_width=1, legend='Average number of votes', line_color='green', muted_alpha=0.1)
    
    # Add legend
    p.legend.location = 'bottom_left'
    p.legend.click_policy = 'mute'

    # Specify output file
    output_file('Show_Graph_{0}.html'.format(show_id))
    
    # Show the graph
    show(p)


def parse_arguments():
    """
    Parses argumnets given by the user and call create_graph() to create and show graph
    """
    # Parser object
    parser = argparse.ArgumentParser()

    # Create source group and assign arguments to it
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('-i', '--id', help='ID of a show on IMDb site.')
    source_group.add_argument('-l', '--link', help='Link to a show on IMDb site.')
    
    # What type of data you want to see
    parser.add_argument('-d', '--data', help='Specify what kind of data are going to be displayed, "rv" = Reviews and Votes, "v" = Only votes and "r" = Only reviews', required=True)

    # Optional arguments
    parser.add_argument('-f', '--file', help='Load data from file.', action='store_true', default=False)
    parser.add_argument('-s', '--save', action='store_true', default=False, help='Save data to file for future use, recommended to avoid re-downloading data unnecesarly.')
    parser.add_argument('-n', '--normalize', help='Normalize data to be in range 0-10, easier to read when displaying number of votes and reviews together. When displaying both graphs together set True as default.', action='store_true', default=False)
    parser.add_argument('-a', '--average', action='store_true', default=False, help='Draw an average value line on a graph.')
    
    # Parse arguments
    args = parser.parse_args()

    # Get show id
    if args.link:
        show_id = retrive_id_from_link(args.link)
    else:
        show_id = args.id
    
    # Get the tv show, also check if it is a tv show
    tv_show = API_IMDb(show_id)

    # Ask user if given ID is correct before starting downloading data from IMDb
    if not args.file:
        is_ok = input('ID refers to {0}, do you want to continue? (Y/N): '.format(tv_show.name))

        if not is_ok.upper() == "Y":
            print("Try again with different ID/link.")
            return

    # Make sure that dataset is correctly choosen
    if not 'r' in args.data and not 'v' in args.data:
        print('Wrong data arguments, pass "r", "v" or "rv". For more info run script with -h flag')
        return

    # Check if user wants to display both reviews and votes together and if yes normalize data as default
    if 'r' in args.data and 'v' in args.data:
        normalize = True
    else:
        normalize = args.normalize

    create_graph(show_id=show_id, save=args.save, normalize=normalize, load_file=args.file, data=args.data, average=args.average, tv_show=tv_show)

if __name__ == '__main__':
    parse_arguments()
