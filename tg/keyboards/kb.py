from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove



CreateButton = KeyboardButton('/Создать')
ListButton = KeyboardButton('/Список_жалоб')

beginBot = ReplyKeyboardMarkup(
    resize_keyboard=True, 
    one_time_keyboard=True).row(CreateButton, ListButton)


autoInput = KeyboardButton('/Автоматически_установить_адрес', request_location=True)
inputType = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(autoInput)


reportDescription = KeyboardButton('/Описать_проблему')
reportMarkup = ReplyKeyboardMarkup(
    resize_keyboard= True,
    one_time_keyboard=True
).add(reportDescription)



inlineChoice = InlineKeyboardMarkup(
).add(InlineKeyboardButton(text='Указать автоматически', callback_data='auto')
      ).add(InlineKeyboardButton(text='Указать вручную', callback_data='manual'))

inlineAccept = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Назад', callback_data='back'))

listReports = KeyboardButton('/Просмотреть_мои_жалобы')
reportsReply = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(listReports)


emptyKeyboard = ReplyKeyboardRemove()



rate1 = InlineKeyboardButton(text='1/5', callback_data='rate1')
rate2 = InlineKeyboardButton(text='2/5', callback_data='rate2')
rate3 = InlineKeyboardButton(text='3/5', callback_data='rate3')
rate4 = InlineKeyboardButton(text='4/5', callback_data='rate4')
rate5 = InlineKeyboardButton(text='5/5', callback_data='rate5')
ratingReply = InlineKeyboardMarkup().row(rate1, rate2, rate3, rate4, rate5)