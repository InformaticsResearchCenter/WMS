from django.shortcuts import render, redirect

from WMS.models import *

from django.http import HttpResponseRedirect

from pprint import pprint

from sequences import get_next_value

from django.db import connection
from django.db import models

from datetime import datetime

# Create your views here.


def scanner(request):
    return render(request, 'storage/index.html')
