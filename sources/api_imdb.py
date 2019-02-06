from imdb import IMDb
import files

def progress_bar(total, current, description, prefix):
    """
    Creates progress bar with description
    """
    lenght = 100
    
    percent = round(float(current) * 100/float(total), 2)
    filled = int(lenght * current // total)
    bar = filled * "#" + "-" * (lenght-filled)

    print("\r{0}: |{1}| {2}% [{3}]".format(prefix, bar, percent, description), end="\r")

    if total == current:
        print("\r")

class API_IMDb():
    def __init__(self, show_id):
        self.show_id = show_id
        self.imdb = IMDb()
    
    def download_reviews(self, save):
        """
        Downloads reviews for a show and returns a dictionary -> {Season1:[]}
        """

        # Get the entire show seasons and episodes, retrives dictionary of dictionaries
        show = self.imdb.get_movie(self.show_id, info=['episodes', 'main']) 
        serie = show['episodes']

        reviews = {}
        current_episode = 0

        # Iterate through every season
        for season, episodes in zip(serie.keys(), serie.values()):
            
            # Iterate through every episode in a season
            for episode_number, episodeObject in zip(episodes.keys(), episodes.values()):
                
                current_episode += 1
                progress_bar(show['number of episodes'], current_episode, "Now downloading Season {0} Episode {1}".format(season, episode_number), "Downloading reviews")

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
            files.save_data_to_file(reviews, "reviews", show['title'].replace(" ", "_"))

        return reviews

    def _download_review_for_episode(self, episode_id):
        """
        Downloads reviews for one episode and returns it
        """
        return self.imdb.get_movie(episode_id, info=['vote details'])['arithmetic mean']

    def download_number_of_votes(self, save):
        """
        Downloads number of votes for a show and returns a dictionary -> {Season1:[]}
        """
        # Get the entire show seasons and episodes, retrives dictionary of dictionaries
        show = self.imdb.get_movie(self.show_id, info=['episodes', 'main']) 
        serie = show['episodes']

        votes = {}
        current_episode = 0

        # Iterate through every season
        for season, episodes in zip(serie.keys(), serie.values()):
            
            # Iterate through every episode in a season
            for episode_number, episodeObject in zip(episodes.keys(), episodes.values()):
                
                current_episode += 1
                progress_bar(show['number of episodes'], current_episode, "Now downloading Season {0} Episode {1}".format(season, episode_number), "Downloading votes")

                # Get episode ID
                episde_id = episodeObject.getID()
                
                # Download votes for episode
                episode_review = self._download_review_for_episode(episde_id)

                # Make sure that the list for this season is created and append that list with episode votes
                if "Season{0}".format(season) in votes.keys():
                    votes["Season{0}".format(season)].append(episode_review)
                else:
                    votes["Season{0}".format(season)] = [episode_review]
        
        # Check if user wants to save data
        if save:
            # Save votes to a file
            files.save_data_to_file(votes, "votes", show['title'].replace(" ", "_"))
        
        return votes


    def _download_number_of_votes_for_episode(self, episode_id):
        """
        Downloads number of votes for one episode and returns it
        """
        return self.imdb.get_movie(episode_id)['votes']
    
    @property
    def is_show(self):
        """
        Checks if given id is a show
        """
        return self.imdb.get_movie(self.show_id)['kind'] == 'tv series'


rev = API_IMDb(2661044).download_reviews(False)
