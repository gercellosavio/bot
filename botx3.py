#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import threading
import shutil
import os
import json
import time
from ipaddress import IPv4Address

import logging
import re
from typing import Dict
from datetime import date
from datetime import datetime
import mysql.connector
from telegram import ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup,Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE,MENU_CABALLO,REALIZAR_APUESTA,MENU_PRINCIPAL,DEPOSITO,RETIRO,MONTO_APUESTA= range(9)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])
caballos=[
            [   
               InlineKeyboardButton("1", callback_data="1"),
               InlineKeyboardButton("2", callback_data="2"),
               InlineKeyboardButton("3", callback_data="3"),
               InlineKeyboardButton("4", callback_data="4")
              
            ]
          ]
carrera_data= [
                [   
                   InlineKeyboardButton("1", callback_data="carrera1"),
                   InlineKeyboardButton("2", callback_data="carrera2")
              
                ]
          ]
reply_keyboard = [
    ['correo', 'clave'],
    ['guardar'],
]
#carrera_data= [['carera', 'carrera1'],['carera2','carera3'],['carera4','carera5',]]
#caballos = [['caballo', 'caaballo1'],['caballo2','caballo3'],['caballo4','caballo5',]]
reply_keyboard_jugar = [['0,00'],['apostar', 'Deposito'],['Retiro','Soporte']]
inicio_jugar = [['seleccione carrera']]
inicio_menu = [['Menu']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
markup_jugar = ReplyKeyboardMarkup(reply_keyboard_jugar, one_time_keyboard=True)
markup_caballos = InlineKeyboardMarkup(caballos)
markup_carreras = InlineKeyboardMarkup(carrera_data)
markup_carreras_ir = ReplyKeyboardMarkup(inicio_jugar, one_time_keyboard=True)
markup_menu_principal = ReplyKeyboardMarkup(inicio_menu, one_time_keyboard=True)



def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""

    update.message.reply_text(
        "bienvenido al bot de apuestas de caballo"
        "  registrar tus datos es importante selecciona en el menu para registrarte",
        reply_markup=markup,
    )
   

    return CHOOSING

def jugar(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user for input."""
    if os.path.exists('caballo.txt'):
     print("archivo encontrado.")
     time.sleep(1)
     t = threading.Timer(3, caballo)
     t.start()
    else:
     print("esperando archivo")
     time.sleep(3)
    update.message.reply_text(
        "",
        reply_markup=markup_carreras_ir,
    )
    


def realizar_apuesta(update: Update, context: CallbackContext) -> int:
    
    query = update.callback_query
    query.answer()
    user_data=context.user_data
    user_data['caballo'] =query.data
    query.edit_message_text(text="seleccione su caballo\n"
          "1)Rodríguez ---J./Gorham M.\n"
          "2)Transfer ---Batista L./Rick B.\n"
          "3)Spritzer---Acosta J./Kee W.\n"
          f"4)Under Fire---Ruiz J./Eppler M.\n*Tu Seleccionaste* {facts_to_str(user_data)} \npor favor digite el monto de la apuesta")
    

    return MONTO_APUESTA 


 



def monto_apuesta(update: Update, context: CallbackContext) -> int:
    user_data=context.user_data
    text = update.message.text
    user_data['apuesta'] = text
    update.message.reply_text(
        f"gracias por realizar su apuesta  {facts_to_str(user_data)}",
        reply_markup=markup_jugar,
    )
    return MENU_PRINCIPAL 


def menuprincipal(update: Update, context: CallbackContext) -> int:
    text = update.message.text 
    if 'Menu'in text:
      update.message.reply_text(
          "gracias por realizar tu registro debes ingresar dineros a tu balance para empezar a apostar ",
          reply_markup=markup_jugar,
       )
      return MENU_PRINCIPAL    
    if 'Deposito'in text:
      update.message.reply_text(
          "digite el codigo de referencia del pago movil recuerde debe ser los ultimos 4 digitos",
          reply_markup=markup_jugar,
         )
      return DEPOSITO
   



    if 'apostar'in text:
      update.message.reply_text(
          "seleccione su caballo\n "
          "1)carrera rinconada\n"
          "2)carrera n° 2\n",
        reply_markup=markup_carreras,
         )
      return MENU_CABALLO

    



    if 'Retiro'in text:
      update.message.reply_text(
          "ingrese su los datos del pago movil ej: banco-spacio-N° de telefono-espacio-N° de cedula-espacio-monto a retirar ------ 0102 04124198621 21531462 90,00 ",
          reply_markup=markup_jugar,
         )
      return RETIRO


def deposito(update: Update, context: CallbackContext) -> int:
    text = update.message.text 
    if text.isdigit() and len(text)==4:
      update.message.reply_text(
          "gracias por realizar tu registro en una hora aproximadamente se vera reflejada en tu balance recuerde si registro el numero de referencia equivocado debera esperar una hora para registrarlo de nuevo ",
          reply_markup=markup_jugar,
       )
      return MENU_PRINCIPAL    
    else: 
      update.message.reply_text(
          "digite el codigo de referencia del pago movil correctamente recuerde debe ser los ultimos 4 digitos ",
          reply_markup=markup_jugar,
         )
      return DEPOSITO

def retiro(update: Update, context: CallbackContext) -> int:
      text = update.message.text 
    
      update.message.reply_text(
          "gracias por registrar su retiro sera procesado ala brevedad ",
          reply_markup=markup_jugar,
       )
      return MENU_PRINCIPAL    
   
def menucaballo(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    user_data=context.user_data
    text=query.data
    user_data['carrera'] = text
    query.edit_message_text(text="seleccione su caballo\n "
          "1)Rodríguez ---J./Gorham M.\n"
          "2)Transfer ---Batista L./Rick B.\n"
          "3)Spritzer---Acosta J./Kee W.\n"
          "4)Under Fire---Ruiz J./Eppler M.\n",
        reply_markup=markup_caballos,
    )

    return REALIZAR_APUESTA

def regular_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text(f'cual es tu {text.lower()}?')

    return TYPING_REPLY


def custom_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom category."""
    update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )

    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    if category == "correo" :
       mydb = mysql.connector.connect(
       host="db4free.net",
       user="test_columbus_2",
       passwd="test_columbus_2",
       database="test_columbus_2")
       mycursor = mydb.cursor()
       mycursor.execute("SELECT nombre FROM usuarios WHERE nombre = '%s'" %text)
       myresult = mycursor.fetchall()
       if myresult:
           update.message.reply_text(f' {myresult[0][0]} este correo ya esta en uso preciona el boton correo para agregar otro correo')
           
       else:
           user_data[category] = text
           del user_data['choice']  
           print(user_data) 
           update.message.reply_text(
            "esta informacion es correcta ?"
            f"{facts_to_str(user_data)} si es asi presiona guardar",
            reply_markup=markup,
            )

    else:
       user_data[category] = text
       del user_data['choice']   
       update.message.reply_text(
        "esta informacion es correcta ?"
        f"{facts_to_str(user_data)} si es asi preciona guardar",
        reply_markup=markup,
        )

    return CHOOSING


def guardar(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    print(user_data)
    if 'choice' in user_data:
        del user_data['choice']
    if  ('clave' in user_data) and ('correo' in user_data):
        
       now = datetime.now()

       update.message.reply_text(
           f"recuerde su informacion  {facts_to_str(user_data)}luego le sera muy util",
           reply_markup=ReplyKeyboardRemove(),
       )
       mydb = mysql.connector.connect(
        host="db4free.net",
        user="test_columbus_2",
        passwd="test_columbus_2",
        database="test_columbus_2"
        )
       mycursor = mydb.cursor()
       sql = "INSERT INTO usuarios (nombre,email,clave,fecha_registro,direccion_billetera,balance,estatus) VALUES ( %s,%s, %s,%s, %s,%s,%s)"
       val = (user_data['correo'],user_data['correo'],user_data['clave'],now,'xxxxxxxx',0.0,'activo')
       mycursor.execute(sql, val)
       mydb.commit()
       print(mycursor.rowcount, "registro insertado")
       user_data.clear()
       update.message.reply_text(
        "seleccione el menu",
        reply_markup=markup_menu_principal,
       )
       return MENU_PRINCIPAL
    else:
        update.message.reply_text(f'falta la clave o correo para seguir con el proceso de registro selecione el dato que le falta ')
        return CHOOSING
    




def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5039897959:AAEBlceAfn4flNvX_IUN29wFR5LXJz1NvpA")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),CommandHandler('APOSTAR', jugar)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(correo|clave)$'), regular_choice
                ),
                MessageHandler(Filters.regex('^Something else...$'), custom_choice),
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^guardar$')), regular_choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^guardar$')),
                    received_information,
                )
            ],
            MENU_CABALLO: [
                CallbackQueryHandler(menucaballo)
                    
                
            ],
             REALIZAR_APUESTA: [
                CallbackQueryHandler(realizar_apuesta)
            ],
            MENU_PRINCIPAL: [
                MessageHandler(
                    Filters.regex('^(Deposito|Retiro|soprte|Menu|apostar)$'),
                    menuprincipal,
                )
            ],
            DEPOSITO: [
                    MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^guardar$')), deposito
                    )
            ],
            MONTO_APUESTA: [
            MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^guardar$')), monto_apuesta
                    ) 
                   
            ],
            RETIRO: [
                    MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^guardar$')), retiro
                    )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^guardar$'), guardar)],
    )


     

    dispatcher.add_handler(conv_handler)


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()