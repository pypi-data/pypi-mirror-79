# SPDX-License-Identifier: Apache-2.0

# Copyright 2020 Contributors to OpenLEADR

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from typing import List
from datetime import datetime, timezone, timedelta

@dataclass
class AggregatedPNode(dict):
    node: str

@dataclass
class EndDeviceAsset(dict):
    mrid: str

@dataclass
class MeterAsset(dict):
    mrid: str

@dataclass
class PNode(dict):
    node: str

@dataclass
class FeatureCollection(dict):
    id: str
    location: dict

@dataclass
class ServiceArea(dict):
    feature_collection: FeatureCollection

@dataclass
class ServiceDeliveryPoint(dict):
    node: str

@dataclass
class ServiceLocation(dict):
    node: str

@dataclass
class TransportInterface(dict):
    point_of_receipt: str
    point_of_delivery: str

@dataclass
class Target(dict):
    aggregated_p_node: AggregatedPNode = None
    end_device_asset: EndDeviceAsset = None
    meter_asset: MeterAsset = None
    p_node: PNode = None
    service_area: ServiceArea = None
    service_delivery_point: ServiceDeliveryPoint = None
    service_location: ServiceLocation = None
    transport_interface: TransportInterface = None
    group_id: str = None
    group_name: str = None
    resource_id: str = None
    ven_id: str = None
    party_id: str = None

@dataclass
class EventDescriptor(dict):
    event_id: int
    modification_number: int
    market_context: str
    event_status: str

    created_date_time: datetime = None
    modification_date: datetime = None
    priority: int = 0
    test_event: bool = False
    vtn_comment: str = None

    def __post_init__(self):
        if self.modification_date is None:
            self.modification_date = datetime.now(timezone.utc)
        if self.created_date_time is None:
            self.created_date_time = datetime.now(timezone.utc)
        if self.modification_number is None:
            self.modification_number = 0
        if not isinstance(self.test_event, bool):
            self.test_event = False

@dataclass
class ActivePeriod(dict):
    dtstart: datetime
    duration: timedelta
    tolerance: dict = None
    notification: dict = None
    ramp_up: dict = None
    recovery: dict = None

@dataclass
class Interval(dict):
    dtstart: datetime
    duration: timedelta
    uid: int

@dataclass
class EventSignal(dict):
    intervals: List[Interval]
    target: Target
    signal_name: str
    signal_type: str
    signal_id: str
    current_value: float

@dataclass
class Event(dict):
    event_descriptor: EventDescriptor
    active_period: ActivePeriod
    event_signals: EventSignal
    target: Target
