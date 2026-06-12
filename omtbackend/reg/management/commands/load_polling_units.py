import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from reg.models import State, LGA, Ward, PollingUnit


class Command(BaseCommand):
    help = 'Load polling unit data from JSON file'

    def handle(self, *args, **options):
        # Path to your JSON file
        json_path = os.path.join(settings.BASE_DIR, 'static', 'reg', 'data.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for state_data in data:
            # Ensure the state name is correctly formatted
            state_name = state_data['state'].title()
            
            # Create or get the state object
            state_obj, state_created = State.objects.get_or_create(name=state_name)
            if state_created:
                self.stdout.write(f'State {state_name} created.')
            
            for lga_data in state_data['lgas']:
                lga_name = lga_data['lga'].title()

                # Create or get the LGA object
                lga_obj, lga_created = LGA.objects.get_or_create(name=lga_name, state=state_obj)
                if lga_created:
                    self.stdout.write(f'LGA {lga_name} created in {state_name}.')

                for ward_data in lga_data['wards']:
                    ward_name = ward_data['ward'].title()

                    # Create or get the Ward object
                    ward_obj, ward_created = Ward.objects.get_or_create(name=ward_name, lga=lga_obj)
                    if ward_created:
                        self.stdout.write(f'Ward {ward_name} created in {lga_name}.')

                    for pu_name in ward_data['polling_units']:
                        # Create or get the PollingUnit object
                        pu_name = pu_name.title()  # Proper title case
                        polling_unit_obj, pu_created = PollingUnit.objects.get_or_create(name=pu_name, ward=ward_obj)
                        if pu_created:
                            self.stdout.write(f'Polling Unit {pu_name} created in {ward_name}.')

        # Completion message after loading data
        self.stdout.write(self.style.SUCCESS('Polling unit data loaded successfully.'))
