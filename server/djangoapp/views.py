# Uncomment the required imports before adding the code
import json
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    """Handle sign in request."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]

    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data = {"userName": username, "status": "Authenticated"}

    return JsonResponse(response_data)


def logout_request(request):
    """Handle sign out request."""
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    """Handle sign up request."""
    data = json.loads(request.body)
    username = data["userName"]
    password = data["password"]
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("%s is a new user", username)

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})

    return JsonResponse({"userName": username, "error": "Already Registered"})


def get_cars(request):
    """Return a list of car models."""
    if CarModel.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]

    return JsonResponse({"CarModels": cars})


def get_dealerships(request, state="All"):
    """Return dealerships; filter by state if provided."""
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    """Return reviews for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    for review_detail in reviews:
        response = analyze_review_sentiments(review_detail["review"])
        review_detail["sentiment"] = response.get("sentiment") if response else None

    return JsonResponse({"status": 200, "reviews": reviews})


def get_dealer_details(request, dealer_id):
    """Return details for a specific dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})


@csrf_exempt
def add_review(request):
    """Submit a review."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as exc:
        logger.error("Error in posting review: %s", exc)
        return JsonResponse({"status": 401, "message": "Error in posting review"})
