from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import professor
from .forms import SubmissaoForm
from .. import db
from ..models import Usuario, Resumo, Avaliador

def check_professor():
    if not current_user.is_prof:
        abort(403)

@professor.route('/professor', methods=['GET','POST'])
@login_required
def visualizar_resumos():
    check_professor()

    resumo = Resumo.query.all()

    return render_template('professor/resumos.html',
                            resumos=resumo, title='Resumos')

@professor.route('/professor/aprovar', methods=['GET','POST'])
@login_required
def aprovar_resumo(id):
    resumo = Resumo.query.get_or_404(id)

    form = SubmissaoForm(obj=resumo)

    if form.validate_on_submit():
        resumo.situacao = 'Aprovado'

        try:
            db.session.add(resumo)
            db.session.commit()
            flash('Resumo aprovado com sucesso')
        except:
            flash('Error: Nao pode aprovar o resumo')

        return redirect(url_for('professor.list_resumos'))

    return render_template('professor/resumos',action='Aprovar',
                            aprovar_resumo=True, resumo=resumo,
                            title='Aprovar resumo')

@professor.route('/professor/reprovar', methods=['GET','POST'])
@login_required
def reprovar_resumo(id):
    resumo = Resumo.query.get_or_404(id)

    form = SubmissaoForm(obj=resumo)

    if form.validate_on_submit():
        resumo.situacao = 'Reprovado'

        try:
            db.session.add(resumo)
            db.session.commit()
            flash('Resumo reprovado com sucesso')
        except:
            flash('Error: Nao pode reprovar o resumo')

        return redirect(url_for('professor.list_resumos'))

    return render_template('professor/resumos',action='Reprovar',
                            aprovar_resumo=False, resumo=resumo,
                            title='Reprovar resumo')
