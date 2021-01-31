import random
from telegram.ext import run_async, Filters
from telegram import Message, Chat, Update, Bot, MessageEntity
from nightingale import dispatcher
from nightingale.modules.disable import DisableAbleCommandHandler

SFW_STRINGS = (
      "ഇരുട്ട് നിറഞ്ഞ എന്റെ ഈ ജീവിതത്തിലേക്ക് ഒരു തകർച്ചയെ ഓർമ്മിപ്പിക്കാൻ എന്തിന് ഈ ഓട്ടക്കാലണ ആയി നീ വന്നു 😖",
      "നമ്മൾ നമ്മൾ പോലുമറിയാതെ അധോലോകം ആയി മാറിക്കഴിഞ്ഞിരിക്കുന്നു ഷാജിയേട്ടാ...😐",
      "എന്നെ ചീത്ത വിളിക്കു... വേണമെങ്കിൽ നല്ല ഇടി ഇടിക്കു... പക്ഷെ ഉപദേശിക്കരുത്.....😏",
      "ഓ ബ്ലഡി ഗ്രാമവാസീസ്!😡",
      "സീ മാഗ്ഗി ഐ ആം ഗോയിങ് ടു പേ ദി ബിൽ.🤑",
      "പോരുന്നോ എന്റെ കൂടെ!😜",
      "തള്ളെ കലിപ്പ് തീരണില്ലല്ലോ!!🤬",
      "ഞാൻ കണ്ടു...!! കിണ്ടി... കിണ്ടി...!🤣",
      "മോന്തയ്ക്കിട്ട് കൊടുത്തിട്ട് ഒന്ന് എടുത്ത് കാണിച്ചുകൊടുക്ക് അപ്പോൾ കാണും ISI മാർക്ക് 😑",
      "ഡേവീസേട്ട, കിങ്ഫിഷറിണ്ടാ... ചിൽഡ്...! .",
      "പാതിരാത്രിക്ക് നിന്റെ അച്ഛൻ ഉണ്ടാക്കി വെച്ചിരിക്കുന്നോ പൊറോട്ടയും ചിക്കനും....😬",
      "ഇത് ഞങ്ങളുടെ പണിസാധനങ്ങളാ രാജാവേ.🔨⛏",
      "കളിക്കല്ലേ കളിച്ചാൽ ഞാൻ തീറ്റിക്കുമെ പുളിമാങ്ങ....😎",
      "മ്മക്ക് ഓരോ ബിയറാ കാച്ചിയാലോ...🥂",
      "ഓ പിന്നെ നീ ഒക്കെ പ്രേമിക്കുമ്പോൾ അത് പ്രണയം.... നമ്മൾ ഒക്കെ പ്രേമിക്കുമ്പോൾ അത് കമ്പി...😩",
      "കള്ളടിക്കുന്നവനല്ലേ കരിമീനിന്റെ സ്വാദറിയു.....😋",
      "ഡാ വിജയാ നമുക്കെന്താ ഈ ബുദ്ധി നേരത്തെ തോന്നാതിരുന്നത്...!🙄",
      "ഇത്രേം കാലം എവിടെ ആയിരുന്നു....!🥰",
      "ദൈവമേ എന്നെ മാത്രം രക്ഷിക്കണേ....⛪",
      "എനിക്കറിയാം ഇവന്റെ അച്ഛന്റെ പേര് ഭവാനിയമ്മ എന്നാ....😂🤣🤣",
      "ഡാ ദാസാ... ഏതാ ഈ അലവലാതി.....😒",
      "ഉപ്പുമാവിന്റെ ഇംഗ്ലീഷ് സാൾട് മംഗോ ട്രീ.....🤔",
      "മക്കളെ.. രാജസ്ഥാൻ മരുഭൂമിയിലേക്ക് മണല് കയറ്റിവിടാൻ നോക്കല്ലേ.....🥵",
      "നിന്റെ അച്ഛനാടാ പോൾ ബാർബർ....🤒",
      "കാർ എൻജിൻ ഔട്ട് കംപ്ലീറ്റ്‌ലി.....🥵",
      "ഇത് കണ്ണോ അതോ കാന്തമോ...👀",
      "നാലാമത്തെ പെഗ്ഗിൽ ഐസ്‌ക്യൂബ്സ് വീഴുന്നതിനു മുൻപ് ഞാൻ അവിടെ എത്തും.....😉",
      "അവളെ ഓർത്ത് കുടിച്ച കല്ലും നനഞ്ഞ മഴയും വേസ്റ്റ്....💔",
      "എന്നോട് പറ ഐ ലവ് യൂ ന്ന്....😘",
      "അല്ല ഇതാര് വാര്യംപിള്ളിയിലെ മീനാക്ഷി അല്ലയോ... എന്താ മോളെ സ്കൂട്ടറില്....🙈 ",
      "കിട്ടിയ  പെണ്ണും  കാട്ടിയ  പെണ്ണും കൂടെ ഇല്ലേലും ജനിപ്പിച്ച പെണ്ണ് കാണും ആജീവനാന്തം 🤰🤱👩‍👦",
  )

@run_async
def q(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(SFW_STRINGS))
    else:
      message.reply_text(random.choice(SFW_STRINGS))

__help__ = """
- /q  😩
"""

__mod_name__ = "Killing Commands"

Q_HANDLER = DisableAbleCommandHandler("q", q)

dispatcher.add_handler(Q_HANDLER)
