from database import get_user, list_users
from flask import Flask, render_template, request
from genai import ia_decision

app = Flask(__name__)

# Página inicial que lista todos os usuários
@app.route('/')
def index():
    users = list_users()
    return render_template('index.html', users=users)
  
# Página de detalhes do usuário e interação com a IA
@app.route('/user/<user_id>', methods=['GET', 'POST'])
def user_details(user_id):
    user = get_user(user_id)
    if not user:
        return "Usuário não encontrado", 404
    if request.method == 'POST':
        ia_response = ia_decision(user)
        return render_template('user.html', user=user, user_id=user_id, message=ia_response)
    return render_template('user.html', user=user, user_id=user_id)
  
if __name__ == '__main__':
    app.run(debug=True)