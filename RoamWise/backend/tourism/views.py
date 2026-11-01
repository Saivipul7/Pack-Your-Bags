import random, string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Place, Trip, Expense, Vote, BusinessSubmission, ListingReport

SEED = [
 ('Hawa Mahal','Heritage','Palace of Winds with an iconic honeycomb facade.','Pink City',26.9239,75.8267,50,75,'09:00-17:00',['architecture','history','culture'],'Step-free access is limited in historic areas',.5),
 ('City Palace','Heritage','Royal courtyards, museums and historic galleries.','Pink City',26.9258,75.8237,300,120,'09:30-17:00',['history','culture','architecture'],'Some courtyards have uneven stone paths',.6),
 ('Jantar Mantar','Heritage','UNESCO-listed astronomical instruments in an open-air complex.','Pink City',26.9248,75.8246,200,75,'09:00-16:30',['science','history','culture'],'Mostly outdoor; shaded seating is limited',.5),
 ('Albert Hall Museum','Museum','Jaipur museum with art, objects and a striking evening-lit facade.','Rambagh',26.9111,75.8195,100,90,'09:00-17:00',['art','history','culture'],'Ramps available at main entrance',.7),
 ('Bapu Bazaar Walk','Shopping','Browse textiles, crafts and everyday market lanes.','Bapu Bazaar',26.9175,75.8231,0,90,'10:00-20:00',['shopping','crafts','local'],'Busy lanes; step-free route varies',.3),
 ('Anokhi Cafe','Food','Vegetarian-friendly cafe supporting local craft culture.','Amber Road',26.9562,75.8461,450,60,'09:30-18:00',['food','vegetarian','local'],'Accessible seating on ground floor',.6),
 ('Mohan Mahal','Food','Traditional Rajasthani dinner in a dramatic dining room.','Amer',26.9855,75.8513,1200,100,'19:00-22:30',['food','culture','dinner'],'Call ahead for access arrangements',1.2),
 ('Sanjay Sharma Pottery Studio','Workshop','Small-group blue pottery demonstration with a local artisan.','Amer Road',26.9681,75.8388,600,90,'10:00-17:00',['crafts','workshop','local'],'Contact host for step-free access',.4),
 ('Jal Mahal Viewpoint','Nature','Lakeside viewpoint for the Water Palace and birdlife.','Amer Road',26.9538,75.8460,0,40,'06:00-18:00',['nature','photography','quiet'],'Lakeside promenade has uneven sections',.3),
 ('Govind Dev Ji Temple','Culture','Historic temple and a welcoming local cultural landmark.','City Palace',26.9257,75.8216,0,45,'05:00-11:30,17:00-21:00',['culture','quiet','history'],'Shoes removed; dress respectfully',.3),
 ('Chokhi Dhani','Experience','Evening village-style folk performances and regional food.','Tonk Road',26.7887,75.8560,900,180,'17:00-23:00',['food','culture','family'],'Confirm accessible routes before visiting',1.4),
 ('Jaipur Heritage Walk','Local guide','Community-led walking tour through old-city lanes.','Pink City',26.9203,75.8243,750,120,'08:00-17:00',['local','history','walking'],'Ask operator about route length and step-free option',.4),
]

def place_json(p):
 return {'id':p.id,'name':p.name,'category':p.category,'description':p.description,'area':p.area,'lat':p.lat,'lng':p.lng,'price':p.price,'duration':p.duration,'hours':p.hours,'verified':p.verified,'source':p.source,'checked':p.checked,'access':p.access,'tags':p.tags,'booking_url':p.booking_url,'carbon':p.carbon}
def trip_json(t):
 return {'id':t.id,'title':t.title,'destination':t.destination,'days':t.days,'budget':t.budget,'party':t.party,'preferences':t.preferences,'plan':t.plan,'share_code':t.share_code,'expenses':[{'id':e.id,'title':e.title,'amount':e.amount,'payer':e.payer,'currency':e.currency} for e in t.expenses.all()]}

@api_view(['GET'])
def health(_): return Response({'status':'ok','service':'RoamWise API'})

@api_view(['GET'])
def bootstrap(_):
 if not Place.objects.exists():
  for row in SEED:
   name,cat,desc,area,lat,lng,price,duration,hours,tags,access,carbon=row
   Place.objects.create(name=name,category=cat,description=desc,area=area,lat=lat,lng=lng,price=price,duration=duration,hours=hours,tags=tags,access=access,carbon=carbon,booking_url='')
 if not User.objects.filter(username='traveler').exists():
  User.objects.create_user(username='traveler', email='traveler@roamwise.local', password='password123', first_name='Sami', last_name='Patel')
 return Response({'destination':{'name':'Jaipur, India','lat':26.9124,'lng':75.7873,'currency':'INR'},'places':[place_json(p) for p in Place.objects.all().order_by('id')],'languages':['English','हिन्दी','Español','Français'],'emergency':{'police':'112','ambulance':'112','tourist_helpline':'1363'},'demo_mode':True})

def make_plan(data):
 prefs=data.get('preferences',{}); days=max(1,min(int(data.get('days',2)),7)); party=max(1,int(data.get('party',1)))
 maxbudget=max(1,int(data.get('budget',5000)))//party
 interests=[x.lower() for x in prefs.get('interests',[])]; pace=prefs.get('pace','Balanced')
 access=prefs.get('access','')
 candidates=list(Place.objects.all()); ranked=[]
 for p in candidates:
  score=sum(2 for tag in p.tags if any(i in tag or tag in i for i in interests))
  if access and ('step-free' in access.lower() or 'wheelchair' in access.lower()) and ('step-free' in p.access.lower() or 'accessible' in p.access.lower()): score+=2
  score+=random.random()*.15
  ranked.append((score,p))
 ranked.sort(key=lambda x:(-x[0],x[1].price))
 chosen=[]; total=0; limit=2 if pace=='Relaxed' else 4 if pace=='Packed' else 3
 for _,p in ranked:
  if len(chosen)>=days*limit: break
  if p.price+total <= maxbudget*days and p.id not in [x.id for x in chosen]: chosen.append(p); total+=p.price
 if len(chosen)<days: chosen=[p for _,p in ranked[:days*2]]
 plan=[]
 for i in range(days):
  chunk=chosen[i*limit:(i+1)*limit]
  if not chunk: chunk=chosen[i:i+1]
  plan.append({'day':i+1,'label':['Arrival & old city','Culture & crafts','Slow local day','Open discoveries'][i%4],'stops':[{'place':place_json(p),'time':f'{9+j*3:02d}:00'} for j,p in enumerate(chunk)]})
 return plan

@api_view(['POST','GET'])
def trips(request):
 if request.method=='GET': return Response([trip_json(t) for t in Trip.objects.order_by('-id')[:20]])
 d=request.data; prefs=d.get('preferences',{})
 if not Place.objects.exists(): bootstrap(None)
 code='RW-'+''.join(random.choices(string.ascii_uppercase+string.digits,k=6))
 trip=Trip.objects.create(title=d.get('title') or f"{d.get('destination','Jaipur')} discovery trip",destination=d.get('destination','Jaipur, India'),days=max(1,min(int(d.get('days',2)),7)),budget=max(0,int(d.get('budget',5000))),party=max(1,int(d.get('party',1))),preferences=prefs,plan=[] ,share_code=code)
 trip.plan=make_plan(d); trip.save(); return Response(trip_json(trip),status=201)

@api_view(['GET','PATCH'])
def trip_detail(request,trip_id):
 trip=get_object_or_404(Trip,id=trip_id)
 if request.method=='PATCH':
  if 'plan' in request.data: trip.plan=request.data['plan']
  if 'title' in request.data: trip.title=request.data['title']
  if 'party' in request.data: trip.party=max(1,int(request.data['party']))
  trip.save()
 return Response(trip_json(trip))

@api_view(['POST'])
def recover(request,trip_id):
 trip=get_object_or_404(Trip,id=trip_id); d=request.data; failed=int(d.get('place_id',0)); reason=d.get('reason','closure')
 current_ids=[s['place']['id'] for day in trip.plan for s in day['stops']]
 old=Place.objects.filter(id=failed).first(); qs=Place.objects.exclude(id__in=current_ids)
 prefs=trip.preferences; interests=prefs.get('interests',[])
 best=sorted(qs,key=lambda p:(0 if reason=='rain' and ('indoor' in p.tags or p.category in ['Museum','Heritage','Food','Workshop']) else 1,abs(p.price-(old.price if old else 300)),p.id))
 replacement=best[0] if best else Place.objects.exclude(id=failed).first()
 return Response({'reason':reason,'replacement':place_json(replacement) if replacement else None,'time_delta_minutes':int((replacement.duration if replacement else 0)-(old.duration if old else 0)),'cost_delta':(replacement.price if replacement else 0)-(old.price if old else 0),'message':f"Suggested for {reason}; check current hours with the venue."})

@api_view(['POST'])
def expenses(request,trip_id):
 trip=get_object_or_404(Trip,id=trip_id); d=request.data
 e=Expense.objects.create(trip=trip,title=d.get('title','Trip expense'),amount=max(0,float(d.get('amount',0))),payer=d.get('payer','You'),currency=d.get('currency','INR'))
 return Response({'id':e.id,'title':e.title,'amount':e.amount,'payer':e.payer,'currency':e.currency},status=201)

@api_view(['POST'])
def votes(request,trip_id):
 trip=get_object_or_404(Trip,id=trip_id); pid=int(request.data.get('place_id',0)); voter=request.data.get('voter','You')[:80]
 try: Vote.objects.create(trip=trip,place_id=pid,voter=voter)
 except IntegrityError: pass
 return Response({'votes':Vote.objects.filter(trip=trip,place_id=pid).count(),'place_id':pid})

@api_view(['POST'])
def business_submissions(request):
 d=request.data
 required=['name','category','area','contact','description']
 if any(not d.get(k) for k in required): return Response({'error':'Please complete all fields.'},status=400)
 s=BusinessSubmission.objects.create(**{k:d[k] for k in required})
 return Response({'id':s.id,'status':s.status,'message':'Thanks. Your listing is waiting for local verification.'},status=201)

@api_view(['POST'])
def reports(request):
 d=request.data
 if not d.get('place_id') or not d.get('reason'): return Response({'error':'Choose a listing and a reason.'},status=400)
 report=ListingReport.objects.create(place_id=int(d['place_id']),reason=d['reason'],details=d.get('details',''))
 return Response({'id':report.id,'message':'Report received for review.'},status=201)

@api_view(['POST'])
def assistant(request):
 question=request.data.get('question','').strip()
 if not question: return Response({'error':'Ask a question first.'},status=400)
 q=question.lower(); places=list(Place.objects.all());
 keywords=[w for w in q.replace('?','').replace(',','').split() if len(w)>3]
 matches=[p for p in places if any(k in p.name.lower() or k in p.description.lower() or k in ' '.join(p.tags).lower() or k in p.category.lower() for k in keywords)]
 if any(w in q for w in ['vegetarian','vegan','food','eat','lunch','dinner','cafe','restaurant']): matches=sorted([p for p in places if 'food' in p.tags or p.category=='Food'],key=lambda p:p.price)
 elif any(w in q for w in ['rain','indoors','indoor','museum']): matches=[p for p in places if p.category in ['Museum','Heritage','Food','Workshop']]
 if not matches: matches=sorted(places,key=lambda p:(not p.verified,p.price))[:3]
 picks=matches[:3]
 return Response({'answer':('Here are a few verified listings from this destination guide. Check venue hours before heading out.' if picks else 'I could not find a matching listing in the local guide yet.'),'places':[place_json(p) for p in picks],'grounded':True,'note':'Recommendations use the curated demo directory; this concierge does not check live availability.'})

def user_json(u):
 return {
  'id': u.id,
  'username': u.username,
  'email': u.email,
  'name': (u.first_name + (' ' + u.last_name if u.last_name else '')).strip() or u.username,
  'date_joined': u.date_joined.strftime('%b %d, %Y') if u.date_joined else ''
 }

@api_view(['POST'])
def auth_register(request):
 d = request.data
 username = (d.get('username') or '').strip()
 password = d.get('password') or ''
 email = (d.get('email') or '').strip()
 name = (d.get('name') or '').strip()

 if not username:
  return Response({'error': 'Please choose a username.'}, status=status.HTTP_400_BAD_REQUEST)
 if len(username) < 3:
  return Response({'error': 'Username must be at least 3 characters long.'}, status=status.HTTP_400_BAD_REQUEST)
 if not password:
  return Response({'error': 'Please enter a password.'}, status=status.HTTP_400_BAD_REQUEST)
 if len(password) < 4:
  return Response({'error': 'Password must be at least 4 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

 if User.objects.filter(username__iexact=username).exists():
  return Response({'error': 'An account with that username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

 if email and User.objects.filter(email__iexact=email).exists():
  return Response({'error': 'An account with that email address already exists.'}, status=status.HTTP_400_BAD_REQUEST)

 parts = name.split(' ', 1) if name else [username, '']
 first_name = parts[0]
 last_name = parts[1] if len(parts) > 1 else ''

 user = User.objects.create_user(
  username=username,
  email=email,
  password=password,
  first_name=first_name,
  last_name=last_name
 )
 return Response({
  'user': user_json(user),
  'message': f'Welcome to RoamWise, {user.first_name}!'
 }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def auth_login(request):
 d = request.data
 identifier = (d.get('username') or '').strip()
 password = d.get('password') or ''

 if not identifier or not password:
  return Response({'error': 'Please provide both username/email and password.'}, status=status.HTTP_400_BAD_REQUEST)

 user = User.objects.filter(username__iexact=identifier).first()
 if not user:
  user = User.objects.filter(email__iexact=identifier).first()

 if not user or not user.check_password(password):
  return Response({'error': 'Invalid username/email or password.'}, status=status.HTTP_400_BAD_REQUEST)

 if not user.is_active:
  return Response({'error': 'This account has been disabled.'}, status=status.HTTP_403_FORBIDDEN)

 return Response({
  'user': user_json(user),
  'message': f'Welcome back, {user.first_name or user.username}!'
 })

@api_view(['POST'])
def auth_logout(request):
 return Response({'message': 'Logged out successfully.'})

@api_view(['GET'])
def auth_me(request):
 username = request.query_params.get('username')
 if username:
  user = User.objects.filter(username__iexact=username).first()
  if user:
   return Response({'user': user_json(user)})
 return Response({'user': None})
