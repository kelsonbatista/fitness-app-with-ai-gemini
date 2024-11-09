import os

import google.generativeai as genai
from database import get_user, list_users
from flask import Flask, render_template, request
from functions import (atualizar_envio_fotos, motivar_envio_fotos,
                       oferecer_desconto_primeira_aula, oferecer_plano_anual)

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

magical_if = genai.GenerativeModel("gemini-1.5-flash",
                                   generation_config={"temperature": 0.5},
                                   tools = [
                                     oferecer_plano_anual, 
                                     motivar_envio_fotos, 
                                     atualizar_envio_fotos,
                                     oferecer_desconto_primeira_aula
                                  ])

def ia_decision(user):
    business_rules = """
      Atue como um personal trainer rígido que avalia com pragmatismo a frequência e o
      engajamento dos alunos.
      Quando você for acionada, deverá ler com critério e cuidado os dados de usuário e
      as regras de negócio. Em muitos casos, você deverá oferecer uma simples mensagem de
      encorajamento. Em outros, fará sentido chamar alguma de suas funções. Quando for o
      caso, chame a função correta e construa sua resposta a partir da mensagem que ela
      gerar.
      1. Para usuários que mostram consistência de longo prazo e uso constante do aplicativo, chamar a função
        de oferecer 20% de desconto no plano anual de personal trainer.
      2. Para usuários com baixo engajamento, chamar a função de motivar o envio de 5 fotos consecutivas na
        academia para receber 50% de desconto no primeiro treino com um personal.
      3. Se uma pessoa estiver em campanha de engajamento de envio de fotos, ela não tem consistência.
      4. Se um usuário estiver enviando fotos consecutivas, chamar a função de atualizar a quantidade
        de fotos enviadas. Zerar a contagem se o envio não for consecutivo.
      4. Se alguma resposta for exibida para o usuário, responda como se estivesse falando
        diretamente com ele.
      5. Se uma pessoa já recebeu desconto anual ela não deve receber nenhuma oferta.
      6. Se uma pessoa recebeu o desconto de primeira_aula ela pode receber o desconto anual.
      Lembre-se: manifeste apoio para pessoas com menos frequência, parabenize muita frequência e
        escolha de forma estratégica quem receberá cada desconto.
      """
    user_decision = magical_if.start_chat(enable_automatic_function_calling=True)
    response = user_decision.send_message(f"Dados do usuário: {user}; Regras de negócio: {business_rules}")
    user_decision.send_message(f"Se não tiver chamado nenhuma função, reflita se deve fazê-lo ou não. "
                              "Lembre-se que você é um personal trainer rígido e pragmático.")
    return response.text
  
