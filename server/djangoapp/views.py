from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from .restapis import get_request, analyze_review_sentiments, post_review
from .models import CarMake, CarModel
from .populate import initiate
import logging
import json

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    result = {"userName": username}
    if user is not None:
        login(request, user)
        result = {"userName": username, "status": "Authenticated"}
    return JsonResponse(result)


def logout_request(request):
    auth_logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except BaseException:
        logger.debug("%s is new user", username)

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"userName": username, "error": "Already Registered"})


def get_cars(request):
    if CarMake.objects.count() == 0:
        initiate()
    cars = [car_model.name for car_model in CarModel.objects.all()]
    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = "/fetchDealer/" + str(dealer_id)
    dealership = get_request(endpoint)
    if dealership is None:
        return JsonResponse({
            "status": 500,
            "dealer": {},
            "message": "Failed to fetch dealer"
        })

    dealer_data = {
        "id": dealership.get("id", dealer_id),
        "full_name": dealership.get("full_name", ""),
        "city": dealership.get("city", ""),
        "state": dealership.get("state", ""),
        "st": dealership.get("st", ""),
        "address": dealership.get("address", ""),
        "zip": dealership.get("zip", ""),
        "lat": dealership.get("lat", 0),
        "long": dealership.get("long", 0),
    }
    return JsonResponse({"status": 200, "dealer": dealer_data})


def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = "/fetchReviews/dealer/" + str(dealer_id)
    reviews = get_request(endpoint)
    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail['review'])
        review_detail['sentiment'] = response.get('sentiment', "unknown")
    return JsonResponse({"status": 200, "reviews": reviews})


def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except BaseException:
        return JsonResponse({
            "status": 401,
            "message": "Error in posting review"
        })
