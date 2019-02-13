from bokeh.plotting import figure, output_file, show
from sources.files_io import load_data_from_file
from sources.api_imdb import API_IMDb
from utylities.utylities import prepare_data_for_presentation, normalize_data, retrive_id_from_link, retrive_seasons
import argparse

def get_data_from_file(show_id, save, data):
    """
    Gets raw data from file and handle lack of the file and downloading data if needed
    """
    reviews_raw = None
    votes_raw = None

    if 'r' in data.lower() and 'v' in data.lower():
        # Try to load data from files
        reviews_raw = load_data_from_file('reviews', show_id)
        votes_raw = load_data_from_file('votes', show_id)

        # Check if data was succesfuly loaded, if not download it
        if reviews_raw is None or votes_raw is None:
            # API
            imdb = API_IMDb(show_id)

            # Download both
            data_raw = imdb.download_all_data(save)

            reviews_raw = data_raw[0]
            votes_raw = data_raw[1]
    elif 'r' in data.lower():
        # Try to load data from files
        reviews_raw = load_data_from_file('reviews', show_id)

        if reviews_raw is None:
            # API
            imdb = API_IMDb(show_id)
            
            reviews_raw = imdb.download_reviews(save)
    elif 'v' in data.lower():
        votes_raw = load_data_from_file('votes', show_id)

        if votes_raw is None:
            # API
            imdb = API_IMDb(show_id)
            
            votes_raw = imdb.download_number_of_votes(save)
    
    return (reviews_raw, votes_raw)

def get_data_from_internet(show_id, save, data):
    """
    Gets raw data from imdb API
    """
    imdb = API_IMDb(show_id)
    
    reviews_raw = None
    votes_raw = None
    
    if 'r' in data.lower() and 'v' in data.lower():
        data_raw = imdb.download_all_data(save)

        reviews_raw = data_raw[0]
        votes_raw = data_raw[1]
    elif 'r' in data.lower():
        reviews_raw = imdb.download_reviews(save)
    elif 'v' in data.lower():
        votes_raw = imdb.download_number_of_votes(save)
    
    return (reviews_raw, votes_raw)

def create_graph2(show_id, save, normalize, load_file, data, average, seasons):
    """
    Creates graph from given arguments
    """
    # If seasons not specify set as all
    if seasons is None:
        seasons = range(200)

    reviews_raw = None
    votes_raw = None

    # Get raw data depending on user choice, from files or imdb
    data_raw = get_data_from_file(show_id, save, data) if load_file else get_data_from_internet(show_id, save, data)

    # Set data
    reviews_raw = data_raw[0].get('data', None)
    votes_raw = data_raw[1].get('data', None)

    # Try to get the title of the show from reviews, if can't try from votes and set as show id if can't
    show_name = data_raw[0].get('show_name', data_raw[1].get('show_name', show_id))

    # Prepare data for presentation
    reviews_prepared = prepare_data_for_presentation(reviews_raw, seasons)
    votes_prepared = prepare_data_for_presentation(votes_raw, seasons)

    # Normalize number of votes if needed
    if normalize:
        votes_prepared = normalize_data(votes_prepared)
    
    # Get lables for the graph
    labels = list(reviews_prepared.keys()) if not reviews_prepared is None else list(votes_prepared)

    # Set data range
    if not reviews_prepared is None or normalize:
        data_range = (0, 11)
    else:
        # Set data range as 0-max value + 10% of max value
        data_range = (0, max(reviews_prepared.values()) + (0.1*max(votes_prepared.values())))
    
    # Create graph object
    p = figure(x_range=labels, y_range=data_range, sizing_mode='stretch_both', title=show_name)
    print('Rendering the graph..')

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
    parser.add_argument('--seasons', default=None, help='Specify what seasons ypu want to display, pass START:END, where both start and end are integers')

    # Parse arguments
    print('Parsing arguments..')
    args = parser.parse_args()

    # Get show id
    if args.link:
        print('Retriving ID from a link..')
        show_id = retrive_id_from_link(args.link)
    else:
        show_id = args.id

    # Make sure that dataset is correctly choosen
    if not 'r' in args.data and not 'v' in args.data:
        print('Wrong data arguments, pass "r", "v" or "rv". For more info run script with -h flag')
        return

    # Check if user wants to display both reviews and votes together and if yes normalize data as default
    if 'r' in args.data and 'v' in args.data:
        normalize = True
    else:
        normalize = args.normalize

    # Get seasons
    seasons = retrive_seasons(args.seasons)

    create_graph2(show_id=show_id, save=args.save, normalize=normalize, load_file=args.file, data=args.data, average=args.average, seasons=seasons)

if __name__ == '__main__':
    parse_arguments()
