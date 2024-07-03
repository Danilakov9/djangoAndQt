from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import SensorData
from django.core.paginator import Paginator
import os
from django.db import IntegrityError
from datetime import datetime


@csrf_exempt
def load_data(request):
    if request.method == "POST":
        try:
            file_path = r"C:\Users\Danila\Desktop\71\betterTime(1)\Desktop_Qt_6_5_3_MinGW_64_bit-Release\release\data.json"
            if not os.path.exists(file_path):
                file_path = "data.json"

            with open(file_path, "r") as file:
                data = json.load(file)

            inserted_count = 0
            skipped_count = 0

            # 获取数据库中最后一条记录的 timestamp
            last_record = SensorData.objects.order_by("-timestamp").first()
            last_timestamp_str = last_record.timestamp if last_record else None
            last_timestamp = (
                datetime.strptime(last_timestamp_str, "%Y-%m-%d %H:%M:%S")
                if last_timestamp_str
                else None
            )

            for entry in data:
                timestamp_str = entry.get("Timestamp", "")
                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

                # 如果 timestamp 早于或等于数据库中最后一条记录的 timestamp，则跳过
                if last_timestamp and timestamp <= last_timestamp:
                    skipped_count += 1
                    continue

                if not SensorData.objects.filter(timestamp=timestamp_str).exists():
                    try:
                        SensorData.objects.create(
                            timestamp=timestamp_str,
                            temperature=entry.get("Temperature", ""),
                            humidity=entry.get("Humidity", ""),
                            gas=entry.get("Gas", ""),
                            sensor_id=entry.get("ID", ""),
                        )
                        inserted_count += 1
                    except IntegrityError:
                        skipped_count += 1
                else:
                    skipped_count += 1

            return JsonResponse(
                {
                    "message": "Data processing completed.",
                    "inserted": inserted_count,
                    "skipped": skipped_count,
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def create_sensor_data(request):
    try:
        data = json.loads(request.body)
        sensor_data = SensorData.objects.create(
            timestamp=data.get("timestamp", ""),
            temperature=data.get("temperature", ""),
            humidity=data.get("humidity", ""),
            gas=data.get("gas", ""),
            sensor_id=data.get("sensor_id", ""),
        )
        return JsonResponse(
            {"id": sensor_data.id, "message": "Data created successfully."}, status=201
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def read_sensor_data(request, sensor_data_id):
    try:
        sensor_data = SensorData.objects.get(pk=sensor_data_id)
        data = {
            "id": sensor_data.id,
            "timestamp": sensor_data.timestamp,
            "temperature": sensor_data.temperature,
            "humidity": sensor_data.humidity,
            "gas": sensor_data.gas,
            "sensor_id": sensor_data.sensor_id,
        }
        return JsonResponse(data, status=200)
    except SensorData.DoesNotExist:
        return HttpResponseNotFound("Data not found")


@csrf_exempt
@require_http_methods(["PUT"])
def update_sensor_data(request, sensor_data_id):
    try:
        sensor_data = SensorData.objects.get(pk=sensor_data_id)
        data = json.loads(request.body)
        sensor_data.timestamp = data.get("timestamp", sensor_data.timestamp)
        sensor_data.temperature = data.get("temperature", sensor_data.temperature)
        sensor_data.humidity = data.get("humidity", sensor_data.humidity)
        sensor_data.gas = data.get("gas", sensor_data.gas)
        sensor_data.sensor_id = data.get("sensor_id", sensor_data.sensor_id)
        sensor_data.save()
        return JsonResponse({"message": "Data updated successfully."}, status=200)
    except SensorData.DoesNotExist:
        return HttpResponseNotFound("Data not found")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_sensor_data(request, sensor_data_id):
    try:
        sensor_data = SensorData.objects.get(pk=sensor_data_id)
        sensor_data.delete()
        return JsonResponse({"message": "Data deleted successfully."}, status=200)
    except SensorData.DoesNotExist:
        return HttpResponseNotFound("Data not found")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_sensor_data(request):
    try:
        sensor_data_list = SensorData.objects.all()
        data = [
            {
                "id": sd.id,
                "timestamp": sd.timestamp,
                "temperature": sd.temperature,
                "humidity": sd.humidity,
                "gas": sd.gas,
                "sensor_id": sd.sensor_id,
            }
            for sd in sensor_data_list
        ]
        return JsonResponse(data, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_sensor_data_paginated(request):
    try:
        page_number = int(request.GET.get("page_number", 1))
        page_size = int(request.GET.get("page_size", 10))
        sensor_data_list = SensorData.objects.all()
        paginator = Paginator(sensor_data_list, page_size)
        page_obj = paginator.get_page(page_number)
        data = [
            {
                "id": sd.id,
                "timestamp": sd.timestamp,
                "temperature": sd.temperature,
                "humidity": sd.humidity,
                "gas": sd.gas,
                "sensor_id": sd.sensor_id,
            }
            for sd in page_obj
        ]
        response = {
            "data": data,
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
        }
        return JsonResponse(response, status=200, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_last_sensor_data(request):
    try:
        sensor_data = SensorData.objects.latest("id")
        data = {
            "id": sensor_data.id,
            "timestamp": sensor_data.timestamp,
            "temperature": sensor_data.temperature,
            "humidity": sensor_data.humidity,
            "gas": sensor_data.gas,
            "sensor_id": sensor_data.sensor_id,
        }
        return JsonResponse(data, status=200)
    except SensorData.DoesNotExist:
        return HttpResponseNotFound("No data found")
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
