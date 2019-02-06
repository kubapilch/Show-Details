def retrive_id_from_link(link):
    """
    Parse the link and retrives the id of a show
    """
    # Id of a show/movie in imdb is always after '/tt', if it is not there it is a wrong link
    if not "/tt" in link:
        raise Exception("Invalid link!")

    elements = link.split("/")

    for element in elements:
        if "tt" in element:
            # Id found retrive it and break the loop
            id = int(element[2:])
            break
    else:
        # Didn't find the id
        raise Exception("Invalid link!")

    return id


def normalize_data(data):
    """
    Normalize data to max value 10 and returns
    """
    # Top number in data pack
    top = 0

    # Find top 
    for season in data.values():
        top = max(season) if top < max(season) else top

    data_noramlized = {}

    # Loop through seasons
    for season, votes in zip(data.keys(), data.values()):

        # Loop through each episode and normalize the data
        for vote in votes:
            new_vote = (vote*10)/top

            # Make sure that data_normalize[season] exist and append
            # if not create and assign a list
            if season in data_noramlized.keys():
                data_noramlized[season].append(new_vote)
            else:
                data_noramlized[season] = [new_vote]

    return data_noramlized
