import logging
import requests

from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
base_url = 'https://restcountries.com/v3.1'

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Thanks for choosing us 😊!')

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer('This bot is used to get short information about a country 🌍. \n'
                         'You can search by name, capital or cca code like uzbekistan | tashkent | uz | uzb.')

@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    await message.answer('This bot was created for MohirFest22. Its main purpose is to get brief information 📖 about a country. \n'
                         '☎️ Contact: @husan_eshonqulov')

@dp.message_handler()
async def echo(message: types.Message):
    code = message.text.lower()
    try:
        response = requests.get(f'{base_url}/name/{code}').json()[0]
    except:
        try:
            response = requests.get(f'{base_url}/capital/{code}').json()[0]
        except:
            return await message.reply('Such a state does not exist 🛑.')
    country = {
        'common_name':  get_att_val(get_att_val(response, 'name'), 'common'),
        'official_name': get_att_val(get_att_val(response, 'name'), 'official'),
        'cca2': get_att_val(response, 'cca2'),
        'cca3': get_att_val(response, 'cca3'),
        'ccn3': get_att_val(response, 'ccn3'),
        'is_independent': get_att_val(response, 'independent'),
        'currencies': get_att_val(response, 'currencies'),
        'idd': get_att_val(response, 'idd'),
        'capital': response['capital'][0],
        'region': get_att_val(response, 'region'),
        'subregion': get_att_val(response, 'subregion'),
        'languages': get_att_val(response, 'languages'),
        'latlng': get_att_val(response, 'latlng'),
        'is_landlocked': response['landlocked'],
        'borders': get_att_val(response, 'borders'),
        'area': get_att_val(response, 'area'),
        'flagIcon': get_att_val(response, 'flag'),
        'maps': get_att_val(response, 'googleMaps'),
        'population': get_att_val(response, 'population'),
        'timezones': response['timezones'][0],
        'flag': response['flags']['png'],
        'coatOfArms': response['coatOfArms']['png']
    }
    caption = f"🎯 <b>Official Name:</b> {country['official_name']} \n" \
              f"🏛 <b>Capital:</b> {country['capital']} \n" \
              f"👫 <b>Population:</b> {country['population']} people \n" \
              f"🌐 <b>Region:</b> {country['region']} \n" \
              f"🗺 <b>Subregion:</b> {country['subregion']} \n" \
              f"⛳ <b>Area:</b> {country['area']} km² \n" \
              f"🕐 <b>Time Zones:</b> {country['timezones']} \n" \
              f"🔍 <b>CCA:</b> {country['cca2']}, {country['cca3']} \n" \
              f"🧩 <b>Borders:</b> {country['borders']} \n"
    await message.answer_photo(photo=country['flag'], caption=caption, parse_mode='HTML')

def get_att_val(obj, att):
    if att in obj:
        return obj[att]
    else:
        return ''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)