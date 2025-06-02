from django.db import models

# Create your models here.
from apps.base.entity.client import Client
from apps.base.entity.user import User, EmailVerification
from apps.base.entity.victim import Victim, Aggression, Phone, PhoneActivation
from apps.base.entity.license import License