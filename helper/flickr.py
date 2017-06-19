from flickrapi import FlickrAPI
import os

def get_location_image(location):
    """Return a photo from Flickr searching by location name."""

    flickr = FlickrAPI(os.environ['FLICKR_KEY'], os.environ['FLICKR_SECRET'], format='parsed-json')
    photo_info = flickr.photos.search(text=location, per_page=1, sort='relevance')
    photo_dict = photo_info['photos'][u'photo'][0]
    photo_url = 'https://farm' + str(photo_dict['farm']) + '.staticflickr.com/' + photo_dict['server'] + '/' + photo_dict['id'] + '_' + photo_dict['secret'] + '.jpg'

    return photo_url