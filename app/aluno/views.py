from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import aluno
from .forms import SubmissaoForm
from .. import db
from ..models import Usuario, Resumo, Avaliador
from datetime import date
import re

# def check_aluno():
#     if not current_user.is_aluno:
#         abort(403)

def distribuir_resumo(id):
    prof = Usuario.query.filter_by(is_prof=True)
    resumos = Resumo.query.all()
    qtd_a = len(prof)
    qtd_r = len(resumos)
    qtd = qtd_r//qtd_a

    for a in prof:
        if Avaliador.query.all():
            avaliador = Avaliador.query.get_by(a.id)
            if (len(avaliador) <= qtd):
                aux = Avaliador(avaliador=a.id, resumo=id)
                db.session.add(aux)
                db.session.commit()
                return
            else:
                continue
        else:
            aux = Avaliador(avaliador=a.id, resumo=id)
            db.session.add(aux)
            db.session.commit()
            return

# tarefas do aluno

@aluno.route('/aluno', methods=['GET', 'POST'])
@login_required
def visualizar_resumos():
    #check_aluno()

    resumo = Resumo.query.all()

    return render_template('aluno/resumos/resumos.html',
                           resumos=resumo, title="Resumos")
#//////////////////////////////// interminado


@aluno.route('/aluno/submeter', methods=['GET', 'POST'])
@login_required
def submeter_resumo():
    form = SubmissaoForm()
    
    if not verificar_data():
        if form.validate_on_submit():
            if verificarAutor(form.autor.data):
                if verificarTitulo(form.titulo.data):
                    resumo = Resumo(titulo=form.titulo.data, texto=form.texto.data, autor=form.autor.data)
                    try:
                        # add o resumo no banco de dados
                        db.session.add(resumo)
                        db.session.commit()
                        flash('Seu resumo foi submetido com sucesso.')
                        distribuir_resumo(id)
                    except:
                        # caso o resumo já tenha sido submetido
                        flash('Error: O resumo já foi enviado.')

                    # redirect to departments page
                    return redirect(url_for('aluno.visualizar_resumos'))
                else:
                    flash('Error: Titulo invalido.')
            else:
                flash('Error: Nome autor invalido.')
    else:
        flash('Prazo encerrado.')    
    # load resumos template
    return render_template('aluno/resumos/resumo.html', action="Add",add_resumo=True, form=form,title="Submeter resumo")

def verificarAutor(field):
    if not re.search(r"/d",field, re.MULTILINE):
        return True
    return False

def  verificarTitulo(field):
    if not re.search(r"/W", field, re.MULTILINE):
        return True
    return False

def verificar_data():
    dataHoje = date.today()
    data = ''
    if (dataHoje.day < 10) and (dataHoje.month < 10):
        data = '0{}/0{}/{}'.format(dataHoje.day,dataHoje.month, dataHoje.year)
    elif dataHoje.day < 10:
        data = '0{}/{}/{}'.format(dataHoje.day,dataHoje.month, dataHoje.year)
    elif dataHoje.month < 10:
        data = '{}/0{}/{}'.format(dataHoje.day,dataHoje.month, dataHoje.year)
    else:
        data = '{}/{}/{}'.format(dataHoje.day,dataHoje.month, dataHoje.year)
    return data > '15/12/2018'

@aluno.route('/aluno/alterar/<int:id>', methods=['GET', 'POST'])
@login_required
def alterar_resumo(id):
    resumo = Resumo.query.get_or_404(id) #qual nossa modificação?

    form = SubmissaoForm(obj=resumo)

    if not verificar_data(): 
        if form.validate_on_submit():
            resumo.titulo = form.titulo.data
            resumo.texto = form.texto.data
            #resumo.co_autor = form.co_autor.data
            try:
                db.session.add(resumo)
                db.session.commit()
                flash('Resumo alterado com sucesso.')
            except:
                # in case department name already exists
                flash('Error: resumo existente.')

            # redirect to the departments page
            return redirect(url_for('aluno.visualizar_resumos'))
    else:
        flash('Prazo encerrado')


    form.titulo.data = resumo.titulo
    form.texto.data = resumo.texto
    form.co_autor.data = resumo.co_autor 
    return render_template('aluno/resumos/resumo.html', action="Edit",
                           add_resumo=False, form=form,
                           resumo=resumo, title="Editar resumo")

@aluno.route('/aluno/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def apagar_resumo(id):

    if not verificar_data(): 
        resumo = Resumo.query.get_or_404(id)
        db.session.delete(resumo)
        db.session.commit()
        flash('Seu resumo foi apagado com sucesso.')
    else:
        flash('Prazo encerrado')

    return redirect(url_for('aluno.visualizar_resumos'))

#    return render_template(title="Delete Department")