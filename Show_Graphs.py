from bokeh.plotting import figure, output_file, show
from sources.files_io import load_data_from_file
from sources.api_imdb import API_IMDb
from utylities.utylities import prepare_data_for_presentation
from collections import OrderedDict

def create_graph(show_id, save):

    # imdb_api = API_IMDb(show_id=show_id)
    # imdb_api.download_reviews(save)
    reviews_raw = load_data_from_file('reviews', 'The 100')

    # votes_raw = imdb_api.download_number_of_votes(save)

    reviews_data = prepare_data_for_presentation(reviews_raw)



    # votes_data = prepare_data_for_presentation(votes_raw)

    labels = list(reviews_data.keys())
    values_reviews = list(reviews_data.values())
    # values_votes = list(votes_data.values())

    p = figure(x_range=labels, y_range=(0, 10), sizing_mode='stretch_both')


    p.line(labels, values_reviews, line_width=2, legend='Reviews')

    p.legend.location = 'bottom_left'
    p.xaxis.major_label_orientation = 3.14/4
    show(p)

create_graph(2661044, True)