from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from accounts.models import Facility, Ambulance, DriverProfile
from incidents.models import IncidentCategory
from dispatches.models import AmbulanceTariff


class Command(BaseCommand):
    help = "Create a safe J-SEMSAS demo dataset for dashboard/API testing."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="admin@jsemsas.org")

    def handle(self, *args, **options):
        User = get_user_model()
        password = options["password"]
        if len(password) < 12:
            raise CommandError("Password must be at least 12 characters.")

        facility, _ = Facility.objects.get_or_create(
            facility_code="FDU001",
            defaults={"name": "Federal University Dutse Emergency Unit", "address": "Dutse, Jigawa State", "state": "Jigawa", "lga": "Dutse"},
        )
        admin_user, created = User.objects.get_or_create(username=options["username"], defaults={"email": options["email"], "role": User.Roles.SUPER_ADMIN})
        admin_user.email = options["email"]
        admin_user.role = User.Roles.SUPER_ADMIN
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.facility = None
        admin_user.set_password(password)
        admin_user.save()

        driver, _ = User.objects.get_or_create(username="demo.driver", defaults={"first_name": "Demo", "last_name": "Driver", "role": User.Roles.DRIVER, "facility": facility})
        driver.role = User.Roles.DRIVER
        driver.facility = facility
        driver.set_password(password)
        driver.save()
        DriverProfile.objects.get_or_create(user=driver, defaults={"status": DriverProfile.Status.AVAILABLE})

        ambulance, _ = Ambulance.objects.get_or_create(
            ambulance_id="AMB/GHDUTSE/078",
            defaults={"plate_number": "JGW-001-JA", "car_model": "Toyota Hiace", "type": Ambulance.Types.BLS, "facility": facility, "assigned_driver": driver, "equipment_list": ["Oxygen", "First Aid Kit", "Stretcher"]},
        )
        ambulance.assigned_driver = driver
        ambulance.facility = facility
        ambulance.save()

        categories = ["RTA", "Fire Accident", "Gunshot", "SnakeBite", "Maternal Emergency", "Other"]
        for name in categories:
            IncidentCategory.objects.get_or_create(name=name)

        tariffs = {"ALS": 50000, "BLS": 35000, "KEKE": 15000}
        for ambulance_type, amount in tariffs.items():
            AmbulanceTariff.objects.update_or_create(ambulance_type=ambulance_type, defaults={"base_rate": amount, "included_km": 0, "additional_km_rate": 0, "is_active": True})

        self.stdout.write(self.style.SUCCESS("J-SEMSAS demo data is ready."))
        self.stdout.write(f"Admin username: {admin_user.username}")
        self.stdout.write("Demo driver: demo.driver")
        self.stdout.write("Dashboard: /dashboard/")
