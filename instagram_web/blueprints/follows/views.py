from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.follows import Follows
from flask_login import current_user, login_required
import os

follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')

@follows_blueprint.route('/<idol_id>')
@login_required
def create(idol_id):
    idol = User.get_by_id(idol_id)
    if current_user.follow(idol):
        if idol.private:
            flash(f'You\'ve sent a follow request to {idol.username}.','alert alert-success')
        else:
            flash(f'You are now following {idol.username}.','alert alert-success')
        return redirect(url_for('users.show', username=idol.username))
    else:
        flash(f"You can't view {idol.username}'s profile yet.","alert alert-danger")
        return render_template('users/show.html',username=idol.username)

@follows_blueprint.route('/<fan_id>/delete')
@login_required
def destroy(fan_id):
    fan = User.get_by_id(fan_id)
    if fan.unfollow(current_user):
        flash(f'You have rejected the request from {fan.username}.','alert alert-success')
        return redirect(url_for('users.show',username=current_user.username))
    else:
        flash('Something went wrong, try again later.','alert alert-danger')
        return render_template('users/show.html',username=current_user.username)

@follows_blueprint.route('/<idol_id>/unfollow')
@login_required
def unfollow(idol_id):
    idol = User.get_by_id(idol_id)
    if current_user.unfollow(idol):
        flash(f"You have unfollowed {idol.username}.","alert alert-success")
        return redirect(url_for('users.show', username=idol.username))
    else:
        flash(f"Unfollow {idol.username} unsuccesful","alert alert-danger")
        return render_template('users/show.html',username=idol.username)
    
@follows_blueprint.route('/<fan_id>/update')
@login_required
def update(fan_id):
    fan = User.get_by_id(fan_id)
    if current_user.approve_request(fan):
        flash(f'You\'ve approved the follow request from {fan.username}','alert alert-success')
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash(f'Something went wrong, try again later.','alert alert-danger')
        return render_template('users/show.html', username=current_user.username)