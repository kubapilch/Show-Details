from imdb import IMDb
from sources.files_io import save_data_to_file
from datetime import datetime
from collections import OrderedDict
import operator
import sys
from collections import namedtuple

def progress_bar(total, current, description, prefix, show_name):
    """
    Creates progress bar with description
    """
    lenght = 50
    
    percent = round(float(current) * 100/float(total), 2)
    filled = int(lenght * current // total)
    bar = filled * "#" + "-" * (lenght-filled)
    
    done_progress_bar = "\r{0} for {4}: |{1}| {2}% [{3}]".format(prefix, bar, percent, description, show_name)

    # Clear the line before writing
    print( "\r"+ (" " * (len(done_progress_bar) + 2)), end='\r')

    # Print progress bar
    print(done_progress_bar, end="\r")

    # Downloading is done
    if total == current:
        # Clear the line before writing
        print( "\r"+ (" " * (len(done_progress_bar) + 2)), end='\r')
        
        # Print progress bar with cmplete message
        print("\r{0} for {4}: |{1}| {2}% [{3}]".format(prefix, bar, percent, "Completed", show_name))

class API_IMDb():
    def __init__(self, show_id):
        self.show_id = show_id
        self.imdb = IMDb()
        
        # Check if given id refers to a show
        if not self.is_show:
            sys.exit("Given ID/link is not a tv show!")
        
        # Create movie object out of given id
        self.tv_show = self.imdb.get_movie(show_id, info=['episodes', 'main'])
        
        # Get the title of a show
        self.name = self.tv_show['title']
    
    def download_reviews(self, save):
        """
        Downloads reviews for a show and returns a dictionary -> {Season1:[]}
        """
        # Make sure it is a correct show
        self.ask_if_correct_show()

        # Get the entire show seasons and episodes, retrives dictionary of dictionaries
        show = self.tv_show

        # Sort dictionary by season and create OrderedDict out of it
        serie = OrderedDict(sorted(show['episodes'].items(), key=operator.itemgetter(0)))
        
        reviews = OrderedDict()
        current_episode = 0

        # Iterate through every season
        for season, episodes in zip(serie.keys(), serie.values()):
            
            # Iterate through every episode in a season
            for episode_number, episodeObject in zip(episodes.keys(), episodes.values()):
                
                current_episode += 1
                progress_bar(show['number of episodes'], current_episode, "Now downloading Season {0} Episode {1}".format(season, episode_number), "Downloading reviews", self.name)

                # Get episode ID
                episde_id = episodeObject.getID()
                
                # Download review for episode
                episode_review = self._download_review_for_episode(episde_id)

                # Make sure that the list for this season is created and append that list with episode review
                if "Season{0}".format(season) in reviews.keys():
                    reviews["Season{0}".format(season)].append(episode_review)
                else:
                    reviews["Season{0}".format(season)] = [episode_review]
        
        # Check if user wants to save data
        if save:
            # Save reviews to a file
            save_data_to_file(reviews, "reviews", self.show_id)

        return reviews

    def _download_review_for_episode(self, episode_id):
        """
        Downloads reviews for one episode and returns it
        """
        episode = IMDb().get_movie(episode_id, info=['main', 'plot', 'vote details'])

        # Check if episode has been aired already
        if not 'plot' in episode.keys() or datetime.strptime(episode['original air date'], '%d %b %Y') > datetime.now():
            return 0

        return episode['arithmetic mean']

    def download_number_of_votes(self, save):
        """
        Downloads number of votes for a show and returns a dictionary -> {Season1:[]}
        """
        # Make sure it is a correct show
        self.ask_if_correct_show()
        
        # Get the entire show seasons and episodes, retrives dictionary of dictionaries
        show = self.tv_show
        
        # Sort dictionary by season and create OrderedDict out of it
        serie = OrderedDict(sorted(show['episodes'].items(), key=operator.itemgetter(0)))

        votes = OrderedDict()
        current_episode = 0

        # Iterate through every season
        for season, episodes in zip(serie.keys(), serie.values()):
            
            # Iterate through every episode in a season
            for episode_number, episodeObject in zip(episodes.keys(), episodes.values()):
                
                current_episode += 1
                progress_bar(show['number of episodes'], current_episode, "Now downloading Season {0} Episode {1}".format(season, episode_number), "Downloading votes", self.name)

                # Get episode ID
                episde_id = episodeObject.getID()
                
                # Download votes for episode
                episode_review = self._download_number_of_votes_for_episode(episde_id)

                # Make sure that the list for this season is created and append that list with episode votes
                if "Season{0}".format(season) in votes.keys():
                    votes["Season{0}".format(season)].append(episode_review)
                else:
                    votes["Season{0}".format(season)] = [episode_review]
        
        # Check if user wants to save data
        if save:
            # Save votes to a file
            save_data_to_file(votes, "votes", self.show_id)
        
        return votes


    def _download_number_of_votes_for_episode(self, episode_id):
        """
        Downloads number of votes for one episode and returns it
        """
        episode = IMDb().get_movie(episode_id, info=['main', 'plot', 'vote details'])

        # Check if episode has been aired already
        if not 'plot' in episode.keys() or datetime.strptime(episode['original air date'], '%d %b %Y') > datetime.now():
            return 0

        return episode['votes']

    def download_all_data(self, save):
        """
        Downloads numbers of votes and ratings together to shorten the downloading time and improve performance
        """
        # Make sure it is a correct show
        self.ask_if_correct_show()
        
        # Get the entire show seasons and episodes, retrives dictionary of dictionaries
        show = self.tv_show
        
        # Sort dictionary by season and create OrderedDict out of it
        serie = OrderedDict(sorted(show['episodes'].items(), key=operator.itemgetter(0)))

        votes = OrderedDict()
        reviews = OrderedDict()

        current_episode = 0

        # Iterate through every season
        for season, episodes in serie.items():
            
            # Iterate through every episode in a season
            for episode_number, episodeObject in episodes.items():
                
                current_episode += 1
                progress_bar(show['number of episodes'], current_episode, "Now downloading Season {0} Episode {1}".format(season, episode_number), "Downloading data", self.name)

                # Get episode ID
                episde_id = episodeObject.getID()

                # Download data for episode
                episode_data = self._download_all_data_for_episode(episde_id)

                # Make sure that the list of votes for this season is created and append that list with episode votes
                if "Season{0}".format(season) in votes.keys():
                    votes["Season{0}".format(season)].append(episode_data.votes)
                else:
                    votes["Season{0}".format(season)] = [episode_data.votes]
                
                # Make sure that the list of ratings for this season is created and append that list with episode review
                if "Season{0}".format(season) in reviews.keys():
                    reviews["Season{0}".format(season)].append(episode_data.ratings)
                else:
                    reviews["Season{0}".format(season)] = [episode_data.ratings]
        
        if save:
            # Save votes to a file
            save_data_to_file(votes, "votes", self.show_id)

            # Save ratings to a file
            save_data_to_file(reviews, "reviews", self.show_id)
        
        return (reviews, votes)

    def _download_all_data_for_episode(self, episode_id):
        """
        Downloads ratings and number of votes for one episode and returns tuple (ratings, number of votes)
        """
        episode = IMDb().get_movie(episode_id, info=['main', 'plot', 'vote details'])

        # Create named tuple for episode data
        data_episode = namedtuple('data', 'ratings votes')

        # Check if episode has been aired already
        if not 'plot' in episode.keys() or datetime.strptime(episode['original air date'], '%d %b %Y') > datetime.now():
            return data_episode(ratings=0, votes=0)

        return data_episode(ratings=episode['arithmetic mean'], votes=episode['votes'])

    @property
    def is_show(self):
        """
        Checks if given id is a show
        """
        return self.imdb.get_movie(self.show_id)['kind'] == 'tv series'
    
    def ask_if_correct_show(self):
        """
        Ask user if given ID refers to correct tv serie before starting downloading data from IMDb
        """
        is_ok = input('ID refers to {0}, do you want to continue? (Y/N): '.format(self.name))

        if not is_ok.upper() == "Y":
            print("Try again with different ID/link.")
            sys.exit()
