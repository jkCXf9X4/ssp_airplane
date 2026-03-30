#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.CompositeAirframe. Do not edit manually. */

typedef enum Aircraft_CompositeAirframe_ValueReference {
  AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M = 0,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M = 1,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M = 2,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG = 3,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG = 4,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT = 5,
} Aircraft_CompositeAirframe_ValueReference;

#ifdef __cplusplus

inline constexpr size_t Aircraft_CompositeAirframe_VrCount = 6;

struct Aircraft_CompositeAirframe_Instance {
  Aircraft_VrMapping vr_map[6] = {};
  double length_m = 15.0;
  double fuselage_width_m = 3.0;
  double wingspan_m = 10.0;
  int empty_weight_kg = 8573;
  int payload_capacity_kg = 7700;
  int hardpoint_count = 9;
};

inline void Aircraft_CompositeAirframe_initialize_vr_map(Aircraft_CompositeAirframe_Instance* instance) {
  for (size_t i = 0; i < Aircraft_CompositeAirframe_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M] = {&instance->length_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M] = {&instance->fuselage_width_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M] = {&instance->wingspan_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG] = {&instance->empty_weight_kg, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG] = {&instance->payload_capacity_kg, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT] = {&instance->hardpoint_count, AIRCRAFT_DATA_INTEGER, true};
}

#endif  /* __cplusplus */