import csv
from time import sleep
import requests
import datetime as _dt

response = requests.get(
  url='https://proxy.scrapeops.io/v1/',
  params={
      'api_key': 'd26155bf-4a6e-47e7-b42d-303f875cc3f9',
      'url': 'https://quotes.toscrape.com/', 
  },
)

print('Response Body: ', response.content)
      
class EuroparcsAPI:
    def __init__(self) -> None:
        self.ACCOMMODATIONS_data = []
        self.rates_results = []
        self.accommodations_results = []
        self.parcs_results = []
        self.next_year = _dt.datetime.now() + _dt.timedelta(days=365)
        self.session = requests.Session()
    
    def make_request(self, json_data):
        self.headers = {
            'authority': 'api.europarcs.nl',
            'accept': 'application/graphql+json, application/json',
            'accept-language': 'en-US,en;q=0.6',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'country': 'GB',
            'language': 'en',
            'origin': 'https://www.europarcsresorts.com',
            'pragma': 'no-cache',
            'referer': 'https://www.europarcsresorts.com/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        }
        tries = 0
        while tries < 10:
            try : r = self.session.post('https://api.europarcs.nl/api/graphql', headers=self.headers, json=json_data); return r
            except : tries += 1; sleep(5)
    
    def get_ACCOMMODATIONS_list(self):
        print('\nGetting ACCOMMODATIONS List')
        for page in range(1000):
            print('Page', page+1, end= ' ')
            json_data = {
                'query': 'query Search($location: String, $resort: String, $searchType: SearchType!, $page: Int!, $dateMargin: Int!, $startDate: DateInput, $endDate: DateInput, $subjects: [SubjectRequestInput!], $amenities: [AmenityRequestInput!], $minBathroom: Int!, $minBedroom: Int!, $accommodationKinds: [AccommodationKindRequestInput!], $sort: String, $holidayType: HolidayType, $pageSize: Int!, $minPrice: Decimal, $maxPrice: Decimal, $offerCode: String, $durationType: DurationType, $dates: [DateRangeInput], $perSubjectPricing: Boolean) {\n  sortOrders(type: $searchType) {\n    code\n    name\n    __typename\n  }\n  search(\n    query: {searchType: $searchType, location: $location, specificResort: $resort, page: $page, pageSize: $pageSize, dateMargin: $dateMargin, dateFrom: $startDate, dateTo: $endDate, subjects: $subjects, amenities: $amenities, minBathroom: $minBathroom, minBedroom: $minBedroom, accommodationKinds: $accommodationKinds, sort: $sort, holidayType: $holidayType, minPrice: $minPrice, maxPrice: $maxPrice, offerCode: $offerCode, dates: $dates, durationType: $durationType, perSubjectPricing: $perSubjectPricing}\n  ) {\n    aggregateResults {\n      buckets {\n        count\n        image\n        key\n        value\n        __typename\n      }\n      name\n      other\n      __typename\n    }\n    pageNumber\n    pageSize\n    total\n    totalNumberOfPages\n    items {\n      type\n      code\n      description\n      name\n      countrySlug\n      provinceSlug\n      provinceName\n      accommodationKindCode\n      accommodationKindName\n      accommodationKindSlug\n      accommodationSlug\n      acommondationSlug\n      accommodationName\n      slug\n      resortCode\n      id\n      maxSubjects\n      fromNumberOfDays\n      fromPrice\n      forPrice\n      allInFromPrice\n      allInForPrice\n      extra\n      costs {\n        name\n        perSubject\n        perNight\n        isPet\n        price\n        totalPrice\n        count\n        __typename\n      }\n      resortName\n      labelText\n      labelTextColor\n      labelBackgroundColor\n      priceInclusive\n      priceExclusive\n      rating\n      bedrooms\n      bathrooms\n      address {\n        address1\n        city\n        country\n        district\n        latitude\n        longitude\n        __typename\n      }\n      amenities {\n        name\n        image\n        text\n        color\n        code\n        groups {\n          code\n          __typename\n        }\n        __typename\n      }\n      images {\n        mimeType\n        type\n        url\n        urls {\n          key\n          value\n          __typename\n        }\n        __typename\n      }\n      usps\n      offer\n      offerCode\n      arrivalDate\n      departureDate\n      __typename\n    }\n    __typename\n  }\n}\n',
                'operationName': 'Search',
                'variables': {
                    'holidayType': None,
                    'page': page,
                    'pageSize': 100,
                    'searchType': 'ACCOMMODATION_TYPE',
                    'dates': None,
                    'startDate': None,
                    'endDate': None,
                    'dateMargin': 0,
                    'offerCode': None,
                    'amenities': [],
                    'accommodationKinds': [],
                    'minBedroom': 0,
                    'minBathroom': 0,
                    'perSubjectPricing': False,
                },
            }
            r = self.make_request(json_data)
            ACCOMMODATIONS_items = r.json()['data']['search'].get('items', [])
            if not ACCOMMODATIONS_items: ACCOMMODATIONS_items = []
            print(len(ACCOMMODATIONS_items))
            if not len(ACCOMMODATIONS_items) : break
            for ACCOMMODATION_item in ACCOMMODATIONS_items:
                # headers = ['type', 'code', 'description', 'name', 'countrySlug', 'provinceSlug', 'provinceName', 'accommodationKindCode', 'accommodationKindName', 'accommodationKindSlug', 'accommodationSlug', 'acommondationSlug', 'accommodationName', 'slug', 'resortCode', 'id', 'maxSubjects', 'fromNumberOfDays', 'fromPrice', 'forPrice', 'allInFromPrice', 'allInForPrice', 'extra', 'costs', 'resortName', 'labelText', 'labelTextColor', 'labelBackgroundColor', 'priceInclusive', 'priceExclusive', 'rating', 'bedrooms', 'bathrooms', 'address', 'amenities', 'images', 'usps', 'offer', 'offerCode', 'arrivalDate', 'departureDate', '__typename']
                acc_item = dict(ACCOMMODATION_item)
                acc_item['acommondationUrl'] = f'https://www.europarcsresorts.com/holiday-parks/{ACCOMMODATION_item["countrySlug"]}/{ACCOMMODATION_item["provinceSlug"]}/{ACCOMMODATION_item["slug"]}/accommodations/{ACCOMMODATION_item["accommodationKindSlug"]}/{ACCOMMODATION_item["accommodationSlug"]}'
                self.ACCOMMODATIONS_data.append(acc_item)
            if len(ACCOMMODATIONS_items) < 100 : break
        print('\nTotal ACCOMMODATIONS List :', len(self.ACCOMMODATIONS_data))
    
    def get_parcs(self):
        print('\nGetting parcs')
        for p in range(1000):
            json_data_0 = {
                'query': 'query ResortCoordinates {\n  search(\n    query: {searchType: RESORT, page:' + str(p) + ', pageSize: 100, dateMargin: 450, minBathroom: 0, minBedroom: 0}\n  ) {\n    items {\n      name\n      slug\n      countrySlug\n      provinceSlug\n      rating\n      resortCode\n      images {\n        url\n        __typename\n      }\n      address {\n        city\n        country\n        latitude\n        longitude\n        __typename\n      }\n      __typename\n    }\n    total\n    __typename\n  }\n}\n',
                'operationName': 'ResortCoordinates',
                'variables': {},
            }
            resp = self.make_request(json_data_0)
            items = resp.json()['data']['search'].get('items', [])
            if not items: items = []
            if not len(items) : break
            for item in items:
                slug = item['slug']
                rating = item['rating']
                json_data = {
                    'query': 'query ResortDetail($slug: String!, $from: DateTime!, $to: DateTime!) {\n  findResortBySlug(slug: $slug) {\n    countrySlug\n    countryName\n    provinceSlug\n    provinceName\n    slug\n    locResortSlug {\n      key\n      value\n      __typename\n    }\n    locProvinceSlug {\n      key\n      value\n      __typename\n    }\n    locCountrySlug {\n      key\n      value\n      __typename\n    }\n    address {\n      address1\n      city\n      country\n      district\n      latitude\n      longitude\n      houseNumber\n      houseNumberSuffix\n      email\n      phone\n      zipCode\n      __typename\n    }\n    amenityGrp {\n      groupCode\n      groupImage\n      groupName\n      amenities {\n        code\n        name\n        __typename\n      }\n      __typename\n    }\n    amenities {\n      code\n      name\n      __typename\n    }\n    code\n    description\n    facilities\n    fromNumberOfDays\n    fromPrice\n    id\n    images {\n      mimeType\n      type\n      url\n      urls {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    maxSubjects\n    name\n    offerCode\n    ratings {\n      values {\n        type\n        value\n        count\n        __typename\n      }\n      __typename\n    }\n    reviews {\n      name\n      language\n      parkRemark\n      totalScore\n      dateUpdated\n      __typename\n    }\n    resortCode\n    resortMap {\n      filename\n      imageUrl\n      __typename\n    }\n    resortName\n    usps\n    priceInclusive\n    priceExclusive\n    hasRecreatheek\n    __typename\n  }\n  facilities(request: {resortSlug: $slug, from: $from, to: $to}) {\n    code\n    name\n    openingTimes {\n      open\n      close\n      __typename\n    }\n    __typename\n  }\n}\n',
                    'operationName': 'ResortDetail',
                    'variables': {
                        'slug' : slug,
                        'from': '2021-01-25T22:00:00.000Z',
                        'to': '2022-12-30T23:04:04.000Z',
                    },
                }
                response = self.make_request(json_data)
                ResortData = response.json()['data'].get('findResortBySlug', [])
                if not ResortData : ResortData = []
                # ['CATERING', 'CHILD_FRIENDLINESS', 'EMPLOYEES', 'HOSPITALITY', 'LOCATION', 'OVERALL']
                parcs_item = {
                    'Parc_ID' : ResortData['resortCode'],
                    'Parc_Name' : ResortData['resortName'],
                    'Parc_Address' : ResortData['address']['address1'],
                    'Parc-Postalcode' : ResortData['address']['zipCode'],
                    'Parc_City' : ResortData['address']['city'],
                    'Parc_State' : ResortData['provinceName'],
                    'Parc_Country' : ResortData['address']['country'],
                    'Parc_Country_Name' : ResortData['countryName'],
                    'Parc_Stars' : rating,
                    'Parc_Votes' : 0,
                    'Parc_Lat' : float(ResortData['address']['latitude']),
                    'Parc_Lon' : float(ResortData['address']['longitude']),
                    'Parc_nrReviews' : len(ResortData['reviews']),
                    'Parc_GenRating' : 0,
                    'Parc_CateringRating' : 0,
                    'Parc_ChildRating' : 0,
                    'Parc_StaffRating' : 0,
                    'Parc_HospitalityRating' : 0,
                    'Parc_LocationRating' : 0,
                }
                if ResortData['ratings']:
                    for rate in ResortData['ratings']['values']:
                        if   rate['type'] == 'OVERALL' :
                            parcs_item['Parc_GenRating'] = rate['value']
                            parcs_item['Parc_Votes'] = rate['count']
                        elif rate['type'] == 'LOCATION' : parcs_item['Parc_LocationRating'] = rate['value']
                        elif rate['type'] == 'EMPLOYEES' : parcs_item['Parc_StaffRating'] = rate['value']
                        elif rate['type'] == 'HOSPITALITY' : parcs_item['Parc_HospitalityRating'] = rate['value']
                        elif rate['type'] == 'CHILD_FRIENDLINESS' : parcs_item['Parc_ChildRating'] = rate['value']
                        elif rate['type'] == 'CATERING' : parcs_item['Parc_CateringRating'] = rate['value']
                self.parcs_results.append(parcs_item)
            if len(items) < 100 : break
    
    def get_accommodations(self):
        accommodation_item = {
            'Park_ID' : self.ACCOMMODATION['resortCode'],
            'Unit_ID' : self.ACCOMMODATION['id'],
            'Unit_Name' : self.ACCOMMODATION['name'],
            'Park_Name' : self.ACCOMMODATION['resortName'],
            'Unit_Type' : self.ACCOMMODATION['accommodationKindName'],
            'Unit_Size' : '', 
            'Unit_Bedrooms' : self.ACCOMMODATION['bedrooms'],
            'Unit_Bathrooms' : self.ACCOMMODATION['bathrooms'],
            'Unit_Pax' : self.ACCOMMODATION['maxSubjects'],
            'Unit_Rating' : self.ACCOMMODATION['rating'],
            'Unit_nrReviews' : 0,
        }
        json_data = {
            'query': 'query AccommodationDetailsByCode($resortSlug: String, $accommodationCode: String) {\n  findAccommodationDetailsBySlug(\n    resortSlug: $resortSlug\n    accommodationCode: $accommodationCode\n  ) {\n    code\n    countrySlug\n    countryName\n    provinceSlug\n    provinceName\n    slug\n    locSlug {\n      key\n      value\n      __typename\n    }\n    locResortSlug {\n      key\n      value\n      __typename\n    }\n    locProvinceSlug {\n      key\n      value\n      __typename\n    }\n    locCountrySlug {\n      key\n      value\n      __typename\n    }\n    locAccommodationSlug {\n      key\n      value\n      __typename\n    }\n    accommodationKindName\n    accommodationKindSlug\n    resortRatings {\n      values {\n        type\n        value\n        __typename\n      }\n      __typename\n    }\n    name\n    ratings {\n      values {\n        type\n        value\n        count\n        __typename\n      }\n      __typename\n    }\n    resortName\n    resortCode\n    reviews {\n      name\n      language\n      parkRemark\n      totalScore\n      dateUpdated\n      __typename\n    }\n    description\n    description2\n    shortDescription\n    maxSubjects\n    maxPets\n    maxBabies\n    maxYoungAdults\n    maxChildren\n    maxAdults\n    resortSlug\n    bedrooms\n    images {\n      mimeType\n      url\n      urls {\n        key\n        value\n        __typename\n      }\n      type\n      __typename\n    }\n    floorPlans {\n      url\n      __typename\n    }\n    address {\n      city\n      country\n      __typename\n    }\n    amenities {\n      code\n      description\n      name\n      __typename\n    }\n    amenityGrp {\n      groupCode\n      groupImage\n      groupName\n      amenities {\n        code\n        name\n        numberValue\n        __typename\n      }\n      __typename\n    }\n    priceInclusive\n    priceExclusive\n    __typename\n  }\n  content(\n    table: "accommodation"\n    filter: [{field: "resortSlug", value: {string: $resortSlug}}, {field: "accommodationSlug", value: {string: $accommodationCode}}]\n  ) {\n    data {\n      id\n      data\n      indexKeys {\n        key\n        value\n        __typename\n      }\n      slug {\n        key\n        value\n        __typename\n      }\n      __typename\n    }\n    includedData {\n      id\n      data\n      type\n      __typename\n    }\n    __typename\n  }\n}\n',
            'operationName': 'AccommodationDetailsByCode',
            'variables': {
                'resortSlug': self.ACCOMMODATION['slug'],
                'accommodationCode': self.ACCOMMODATION['acommondationSlug'],
            },
        }
        AccommodationDetailsResponse = self.make_request(json_data)
        try:
            AccommodationDetails = AccommodationDetailsResponse.json()['data'].get('findAccommodationDetailsBySlug')
        except requests.exceptions.JSONDecodeError:
            AccommodationDetailsResponse = self.make_request(json_data)
            AccommodationDetails = AccommodationDetailsResponse.json()['data'].get('findAccommodationDetailsBySlug')
        
        if not AccommodationDetails : AccommodationDetails = {'reviews': [], 'amenityGrp':[]}
        accommodation_item['Unit_nrReviews'] = len(AccommodationDetails['reviews'])
        for amenityGrp in AccommodationDetails['amenityGrp']:
            for amenity in amenityGrp['amenities']:
                if amenity['name'] == 'm² Surface area' or amenity['code'] == 'opp':
                    accommodation_item['Unit_Size'] = amenity['numberValue']
        self.accommodations_results.append(accommodation_item)
    
    def get_data(self):
        self.get_ACCOMMODATIONS_list()
        print('\nGetting Rates and Accommodations')
        print(f'Scanning {len(self.ACCOMMODATIONS_data)} ACCOMMODATIONS\n')
        
        for A, ACCOMMODATION in enumerate(self.ACCOMMODATIONS_data[:], 1):
            AccommodationAvailability_list = []
            print(f'{A} of {len(self.ACCOMMODATIONS_data)} {ACCOMMODATION["name"]}', flush=True)
            self.ACCOMMODATION = ACCOMMODATION
            json_data = {
                'query': 'query AccommodationAvailability($accommodationCode: String, $startDate: DateInput, $endDate: DateInput, $subjects: [SubjectRequestInput], $resortSlug: String, $unitId: String, $offerCode: String, $perSubjectPricing: Boolean) {\n  accommodationAvailability(\n    accommodationCode: $accommodationCode\n    resortSlug: $resortSlug\n    start: $startDate\n    end: $endDate\n    subjects: $subjects\n    unitId: $unitId\n    offer: $offerCode\n    perSubjectPricing: $perSubjectPricing\n  ) {\n    arrivalDate {\n      day\n      month\n      year\n      __typename\n    }\n    departureDate {\n      day\n      month\n      year\n      __typename\n    }\n    allInPrice\n    price\n    allInOfferPrice\n    offerPrice\n    duration\n    offerName\n    extra\n    costs: cost {\n      name\n      perSubject\n      perNight\n      isPet\n      price\n      totalPrice\n      count\n      __typename\n    }\n    __typename\n  }\n}\n',
                'operationName': 'AccommodationAvailability',
                'variables': {
                    'resortSlug': ACCOMMODATION['slug'],
                    'accommodationCode': ACCOMMODATION['acommondationSlug'],
                    'startDate': None,
                    'endDate': None,
                    'perSubjectPricing': False,
                    'offerCode': None,
                },
            }
            AccommodationAvailabilityResponse = self.make_request(json_data)
            items = AccommodationAvailabilityResponse.json()['data'].get('accommodationAvailability', [])
            if not items: items = []
            AccommodationAvailability_list.extend(items)
            try: next_date = items[-1]['arrivalDate']
            except IndexError: continue
            next_date_date_start = _dt.datetime(year=next_date['year'], month=next_date['month'], day=next_date['day'])
            next_date_date_end = next_date_date_start + _dt.timedelta(days=52)
            while next_date_date_start < self.next_year:
                json_data['variables']['startDate'] = { 'year': next_date_date_start.year, 'month': next_date_date_start.month, 'day': next_date_date_start.day}
                json_data['variables']['endDate'] = {'year': next_date_date_end.year, 'month': next_date_date_end.month, 'day': next_date_date_end.day}
                AccommodationAvailabilityResponse = self.make_request(json_data)
                items = AccommodationAvailabilityResponse.json()['data'].get('accommodationAvailability', [])
                if not items: items = []
                if not len(items) : break
                AccommodationAvailability_list.extend(items)
                try:next_date = items[-1]['arrivalDate']
                except IndexError: break 
                next_date_date_start_new = _dt.datetime(year=next_date['year'], month=next_date['month'], day=next_date['day'])
                if next_date_date_start_new == next_date_date_start : break
                else : next_date_date_start = next_date_date_start_new
                
                next_date_date_end = next_date_date_start + _dt.timedelta(days=52)
            unique_AccommodationAvailability_list = []
            for item in AccommodationAvailability_list:
                if item in unique_AccommodationAvailability_list: continue
                unique_AccommodationAvailability_list.append(item)
            print('AccommodationAvailability_list', len(unique_AccommodationAvailability_list))
            print('Getting "Rates" and "ACCOMMODATIONS".', end = ' ', flush=True)
            for item in unique_AccommodationAvailability_list:
                Lodge_Price = item['offerPrice'] if item.get('offerPrice') else item['price']
                ar_date_day = item['arrivalDate']['day']
                ar_date_month = item['arrivalDate']['month']
                ar_date_year = item['arrivalDate']['year']
                day = _dt.date(year=ar_date_year, month=ar_date_month, day=ar_date_day).strftime('%A')
                
                Nights = item['duration']
                # on arrival day Monday 4 and 7 nights
                # on arrival day Friday 3 nights.
                if (day == 'Monday' and (Nights == 4 or Nights == 7)) or (day == 'Friday' and Nights == 3) :
                    # print(f"{ar_date_year}-{ar_date_month}-{ar_date_day}",day, Nights, 'Nights, Unit_ID:', ACCOMMODATION['id'])
                    rate_item = {
                        # 'acommondationUrl': ACCOMMODATION['acommondationUrl'],
                        'Park_ID':ACCOMMODATION['resortCode'],
                        'Unit_ID':ACCOMMODATION['id'],
                        'A_Day' : day,
                        'A_Date': f"{ar_date_year}-{ar_date_month}-{ar_date_day}",
                        'Scrape_Date': _dt.datetime.now().date().__str__(),
                        'Lodge_Price' : float(item['offerPrice'] if item['offerPrice'] else item['price']),
                        'Total_Price' : round((Lodge_Price + sum([float(cost['totalPrice']) for cost in item['costs']])),2),
                        'Nights': Nights
                    }
                    self.rates_results.append(rate_item)
            self.get_accommodations()
            print('Done.')
        self.get_parcs()
        self.session.close()
    
    def save_csv_file(self, file_name, data):
        with open(file_name, 'w', encoding='utf-8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter=',')
            csv_writer.writeheader()
            csv_writer.writerows(data)
    
    def save_data(self):
        print('\nSaving the data')
        if len(self.rates_results):
            self.save_csv_file('Rates Data'+str(datetime.now())+'.csv', self.rates_results)
        
        if len(self.accommodations_results):
            self.save_csv_file('Accommodations Data 011121.csv', self.accommodations_results)
        
        if len(self.parcs_results):
            self.save_csv_file('Parcs Data.csv', self.parcs_results)
    
    def main(self):
        try:
            self.get_data()
        finally:
            self.save_data()

if __name__ == "__main__":
    EuroparcsAPI().main()
