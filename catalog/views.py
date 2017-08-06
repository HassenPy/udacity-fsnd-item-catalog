"""Catalog views."""
from flask import Blueprint, render_template, request, redirect, session, abort
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import db

from auth.models import User
from .models import Pick, Community

catalogApp = Blueprint('catalogApp', __name__)


@catalogApp.route('/', methods=['GET'])
def home():
    """Render the home page with latest picks."""
    communities = Community.query.limit(5).all()
    picks = Pick.query.order_by(Pick.created.desc()).limit(5).all()
    return render_template(
        'home.html',
        communities=communities,
        picks=picks
    )


@catalogApp.route('/community/', methods=['GET'])
def community_list():
    """Render a list with all the communities."""
    communities = Community.query.all()
    return render_template(
        'communityList.html',
        communities=communities,
    )


@catalogApp.route('/community/<int:id>/', methods=['GET'])
def community_page(id):
    """Return a community page with paginated picks."""
    community = Community.query.get(id)
    offset = request.args.get('o', 1)
    communities = Community.query.limit(5).all()
    if not community:
        abort(404)

    # check if passed offset is an integer
    try:
        offset = int(offset)
    except ValueError:
        offset = 1

    if community:
        # Fetch paginated community picks
        picks = Pick.query.filter_by(community=id).paginate(offset, 10)
        return render_template(
            'community.html',
            community=community,
            picks=picks,
            communities=communities
        )
    return render_template(
        'community.html',
        community=community,
        picks=picks,
        communities=communities
    )


@catalogApp.route('/pick/add/', methods=['GET', 'POST'])
@login_required
def pick_add():
    """Handle adding a new pick."""
    communities = Community.query.all()
    title = request.form.get('title', '')
    link = request.form.get('link', '')
    community = request.form.get('community', '')
    try:
        community = int(community)
    except ValueError:
        community = ''
    fields = {'title': title, 'link': link, 'community': community}

    if request.method == 'POST':
        # Check if required fields exist in POST values.
        if not (title and link and community):
            return render_template(
                'pickAdd.html',
                fields=fields,
                communities=communities,
                error="all fields are required",
                errors=None
            )

        pick = Pick(title=title, link=link,
                    community=community, author=session['user_id'])
        if pick.is_valid():
            try:
                db.session.add(pick)
                db.session.commit()
                return redirect('/')
            except IntegrityError:
                db.session.rollback()
                return render_template(
                    'pickAdd.html',
                    communities=communities,
                    fields=fields,
                    error=None,
                    errors={'title': ['a Pick with same title already exists']}
                )
        return render_template(
            'pickAdd.html',
            communities=communities,
            fields=fields,
            error=None,
            errors=pick.errors
        )
    return render_template(
        'pickAdd.html',
        communities=communities,
        fields=fields,
        error=None,
        errors=None
    )


@catalogApp.route('/pick/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def pick_edit(id):
    """Handle editing an existing pick."""
    pick = Pick.query.get(id)
    if not pick:
        abort(404)
    communities = Community.query.all()

    # Check permission
    user_id = session.get('user_id', False)
    if user_id:
        admin = User.query.get(user_id).admin

    if (pick.author != user_id) and not admin:
        abort(401)

    if request.method == 'POST':
        # Check if required fields exist in POST values.
        title = request.form.get('title', '')
        link = request.form.get('link', '')
        community = request.form.get('community', '')
        # a little type conversion for template comparison
        try:
            community = int(community)
        except ValueError:
            community = ''

        if not (title and link and community):
            return render_template(
                'pickEdit.html',
                pick=pick,
                communities=communities,
                error="all fields are required",
                errors=None
            )

        # This is required to prevent automatic flushes
        # This is used since if you post with a non-existant community id
        # you will get a community field insert error on .is_valid() call.
        with db.session.no_autoflush:
            pick.title = title
            pick.link = link
            pick.community = community
            is_valid = pick.is_valid()

        if is_valid:
            try:
                db.session.commit()
                return redirect('/')
            except IntegrityError:
                db.session.rollback()
                return render_template(
                    'pickEdit.html',
                    communities=communities,
                    pick=pick,
                    error=None,
                    errors={'title': ['a Pick with same title already exists']}
                )
        return render_template(
            'pickEdit.html',
            communities=communities,
            pick=pick,
            error=None,
            errors=pick.errors
        )
    return render_template(
        'pickEdit.html',
        communities=communities,
        pick=pick,
        error=None,
        errors=None
    )


@catalogApp.route('/profile/', methods=['GET'])
@login_required
def user_profile():
    """Render the user profile showing his shared picks."""
    user_id = session['user_id']
    picks = Pick.query.filter_by(author=user_id).all()
    return render_template(
        'profile.html',
        picks=picks
    )
