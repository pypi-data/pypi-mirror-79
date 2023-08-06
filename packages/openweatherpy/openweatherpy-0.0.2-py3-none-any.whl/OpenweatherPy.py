
import requests


class WeatherPy:
   def __init__( self, api_key, **kwargs ):
       self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
       self.sample_url = "https://samples.openweathermap.org/data/2.5/weather?"
       self.api_key = api_key
       self.unit = "kelvin"
       self.lang = "en"

       for key, value in kwargs.items():
           if key == "unit":
              if value.upper() == "CELSIUS":
                 self.unit = "metric"
              elif value.upper() == "FAHRENHEIT":
                 self.unit = "imperial"
           elif key == "lang":
              self.lang = value
           else:
              raise Exception(f"Weather class has no keyword \'{key}\'.")
       
   def data_request( self, complete_url ):
       try:
          request = requests.get(complete_url)
          data = request.json()
          if data["cod"] == 200:
             return data
          else:
             return False
       except Exception as e:
          print(e)

   #def zip( self, code ):
       #complete_url = self.sample_url + "zip=" + str(code) + "&appid=" + self.api_key
      # print(complete_url)
      # data = self.data_request(complete_url)
      # if data:
          #data = Info(data)
        #  return data
     #  else:
        #  raise Exception(f"Data for zipcode \'{code}\' not found!")
   
   def query( self, **kwargs ):
       q = ''
       temp_url = self.base_url + "appid=" + self.api_key + "&units=" + self.unit + "&lang=" + self.lang

       city, country, state_code = '', '', ''
       for key, value in kwargs.items():
           if key == 'city':
              city = f'{value}'
           elif key == 'country':
              country = f'{value}'
           elif key == 'state_code':
              state_code = f'{value}'
           else:
              raise Exception(f'query method has no keyword \'{key}\'')

       q = f'{city},{state_code},{country}'.replace(',,',',')

       if q:
          if q[-1] == ',':
             q = q[:-1]
          if q[0] == ',':
             q = q[1:]
       else:
          raise Exception(f'Query is blank!')

       complete_url = temp_url + "&q=" + q

       data = self.data_request(complete_url)
       if data:
          data = Info(data)
          return data
       else:
          raise Exception(f'Query \'{q}\' not found!')
          
   def byId( self, id ):
       complete_url = self.base_url + "appid=" + self.api_key + "&id=" + str(id) + "&units=" + self.unit + "&lang=" + self.lang
       data = self.data_request(complete_url)
       if data:
          data = Info(data)
          return data
       else:
          raise Exception('Invalid id number!')
          
   def languages( self ):
       langs = {
          'af': 'Afrikaans',
          'al': 'Albanian',
          'ar': 'Arabic',
          'az': 'Azerbaijani',
          'bg': 'Bulgarian',
          'ca': 'Catalan',
          'cz': 'Czech',
          'da': 'Danish',
          'de': 'German',
          'el': 'Greek',
          'en': 'English',
          'eu': 'Basque',
          'fa': 'Persian(Farsi)',
          'fi': 'Finnish',
          'fr': 'French',
          'gl': 'Galician',
          'he': 'Hebrew',
          'hi': 'Hindi',
          'hr': 'Croatian',
          'hu': 'Hungarian',
          'id': 'Indonesian',
          'it': 'Italian',
          'ja': 'Japanese',
          'kr': 'Korean',
          'la': 'Latvian',
          'lt': 'Lithuanian',
          'mk': 'Macedonian',
          'no': 'Norwegian',
          'nl': 'Dutch',
          'pl': 'Polish',
          'pt': 'Portuguese',
          'pt_br': 'Português Brasil',
          'ro': 'Romanian',
          'ru': 'Russian',
          'sv, se': 'Swedish',
          'sl': 'Slovenian',
          'sp, es': 'Spanish',
          'sr': 'Serbian',
          'th': 'Thai',
          'tr': 'Turkish',
          'ua, uk': 'Ukranian',
          'vi': 'Vietnamese',
          'zu': 'Zulu',
       }
       return langs

   def coords( self, lon, lat ):
       complete_url = self.base_url + "appid=" + self.api_key + "&lat=" + str(lat) + "&lon=" + str(lon) + "&units=" + self.unit + "&lang=" + self.lang
       data = self.data_request(complete_url)
       if data:
          data = Info(data)
          return data
       else:
          raise Exception('Invalid co-ordinates!')
       
class Info:
   def __init__( self, data ):
       self.name = data["name"]
       self.weather = data["weather"][0]["main"]
       self.description = data["weather"][0]["description"]
       self.temperature = float(self.main(data)["temp"])
       self.pressure = float(self.main(data)["pressure"])
       self.humidity = float(self.main(data)["humidity"])
       self.temp_max = float(self.main(data)["temp_max"])
       self.temp_min = float(self.main(data)["temp_min"])
       self.clouds = data["clouds"]
       self.co_ordinates = self.coords(data)
       self.sunrise = int(data["sys"]["sunrise"])
       self.sunset = int(data["sys"]["sunset"])
       self.id = int(data["id"])
       self.timezone = int(data["timezone"])
       self.wind = self.wind(data)

   def main( self, data ):
       return data["main"]

   def wind( self, data ):
       return data["wind"]
       
   def coords( self, data ):
       return data["coord"]
       
   def __str__( self ):
       return str(self.name)


