from django.shortcuts import render, redirect
from .forms import UserGroup,User, Role
from .models import User,UserGroup,Role
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
from sequences import get_next_value
from django.http import HttpResponseNotFound,HttpResponse
from django.core.exceptions import PermissionDenied
from pprint import pprint
import datetime



def index(request):

    return render(request, 'inside/wmsHomepage/indexs.html')

