import flickrapi
import json, csv, time

api_key = 'adfb5cde5ef4385f544602f4b14dad2f'
api_secret = '6c2ba708522140ba'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

page=1

writer=csv.writer(open("Flickr_Data.csv",'wb'))


while page<401:
	time.sleep(0.1)
	photos = flickr.photos.search(tags='mumbai, travel', tag_mode='all', has_geo='1', per_page=20, page=page)

	#photo_id = photos['photos']['photo'][0]['id']

	#print photo_id

	ph_inc_counter = 0

	while ph_inc_counter<20:
		
		#print ph_inc_counter
		photo_id = photos['photos']['photo'][ph_inc_counter]['id']
		user_id = photos['photos']['photo'][ph_inc_counter]['owner']
		secret = photos['photos']['photo'][ph_inc_counter]['secret']

		# print photo_id, user_id, secret

		location = flickr.photos.geo.getLocation(photo_id=photo_id)
		
		lat = location['photo']['location']['latitude']
		lon = location['photo']['location']['longitude']

		#print lat, lon

		photo_info = flickr.photos.getInfo(photo_id=photo_id, secret=secret)		
		
		timestamp = photo_info['photo']['dates']['taken']
		# print timestamp

		tags = photo_info['photo']['tags']['tag']

		json_data = json.dumps(tags)
		tags_dict = json.loads(json_data)
		tag_strings=""

		tag_inc_counter=0
		while tag_inc_counter < len(tags_dict):
			tag_strings += tags[tag_inc_counter]['_content'] + ', '
			tag_inc_counter+=1

		if tag_strings.endswith(', '):
			tag_strings = tag_strings[:-2]
		#print tag_strings

		info_list = [str(ph_inc_counter), photo_id.encode('utf-8'), user_id.encode('utf-8'), lat.encode('utf-8'), lon.encode('utf-8'), timestamp.encode('utf-8'), tag_strings.encode('utf-8')]

		print str(ph_inc_counter) + ', ' + photo_id.encode('utf-8') + ', ' + user_id.encode('utf-8') + ', ' + lat.encode('utf-8') + ', ' + lon.encode('utf-8') + ', ' + timestamp.encode('utf-8') + ', ' + tag_strings.encode('utf-8')
		writer.writerow(info_list)

		ph_inc_counter+=1

	page+=1


	