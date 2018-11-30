from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import aluno
from .forms import SubmissaoForm
from .. import db
from ..models import Usuario, Resumo

# def check_aluno():
#     if not current_user.is_aluno:
#         abort(403)

# tarefas do aluno

@aluno.route('/aluno', methods=['GET', 'POST'])
@login_required
def visualizar_resumos():
    #check_aluno()

    resumo = Resumo.query.all()

    return render_template('aluno/resumos/resumos.html',
                           resumo=resumo, title="Resumos")
#//////////////////////////////// interminado


@aluno.route('/aluno/submeter', methods=['GET', 'POST'])
@login_required
def submeter_resumo():

    add_resumo = True

    form = SubmissaoForm()
    
    if form.validate_on_submit():
        resumo = Resumo(titulo=form.titulo.data,
                                resumo=form.texto.data,
                                autor=form.autor.data)
        try:
            # add o resumo no banco de dados
            db.session.add(resumo)
            db.session.commit()
            flash('Seu resumo foi submetido com sucesso.')
        except:
            # caso o resumo já tenha sido submetido
            flash('Error: O resumo já foi enviado.')

        # redirect to departments page
        return redirect(url_for('aluno.list_resumos'))

    # load department template
    return render_template('aluno/resumos/resumo.html', action="Add",
                           add_resumo=add_resumo, form=form,
                           title="Submeter resumo")

@aluno.route('/aluno/alterar/<int:id>', methods=['GET', 'POST'])
@login_required
def alterar_resumo(id):

    add_resumo = False

    resumo = Resumo.query.get_or_404(id) #qual nossa modificação?

    form = SubmissaoForm(obj=resumo)

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
        return redirect(url_for('aluno.list_resumos'))

    form.titulo.data = resumo.titulo
    form.texto.data = resumo.texto
    form.co_autor.data = resumo.co_autor 
    return render_template('aluno/resumos/resumo.html', action="Edit",
                           add_resumo=add_resumo, form=form,
                           resumo=resumo, title="Editar resumo")

@aluno.route('/aluno/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def apagar_resumo(id):

    resumo = Resumo.query.get_or_404(id)
    db.session.delete(resumo)
    db.session.commit()
    flash('Seu resumo foi apagado com sucesso.')

    return redirect(url_for('aluno.list_resumos'))

#    return render_template(title="Delete Department")