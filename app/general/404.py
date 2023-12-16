
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@login_required
def template_not_found(e):
    return not_found(e)

@app.errorhandler(404)
@login_required
def not_found(e):
    return render_template('404.html')